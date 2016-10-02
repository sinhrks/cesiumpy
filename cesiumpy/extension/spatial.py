#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals

import collections

from cesiumpy.entities.entity import Polygon, Polyline
import cesiumpy.util.common as com


class _Spatial(object):

    @property
    def _np(self):
        return com._check_package('numpy')

    @property
    def _spatial(self):
        return com._check_package('scipy.spatial')

    @property
    def _geometry(self):
        return com._check_package('shapely.geometry')


class Voronoi(_Spatial):
    """
    Wrapper for scipy.spatial.Voronoi

    Parameters
    ----------

    vor : Voronoi of list of points
    """

    def __init__(self, vor):

        if isinstance(vor, self._spatial.qhull.Voronoi):
            pass
        else:
            vor = self._spatial.Voronoi(vor)

        if vor.points.shape[1] != 2:
            raise ValueError("input must be 2 dimentional points or Voronoi instance")

        self.vor = vor

    def get_polygons(self):
        coordinates = self._get_coordinates()
        polygons = []
        for c in coordinates:
            try:
                polygons.append(Polygon(hierarchy=c))
            except TypeError:
                polygons.append(None)
        return polygons

    def _get_coordinates(self):

        # based on:
        # http://stackoverflow.com/questions/20515554/colorize-voronoi-diagram
        # http://stackoverflow.com/questions/28665491/getting-a-bounded-polygon-coordinates-from-voronoi-cells

        # calculate the center of the area
        center = self.vor.points.mean(axis=0)
        span = self.vor.points.ptp(axis=0)
        radius = span.max()
        span = span / 1.5

        bbox = [[center[0] - span[0], center[1] - span[1]],
                [center[0] + span[0], center[1] - span[1]],
                [center[0] + span[0], center[1] + span[1]],
                [center[0] - span[0], center[1] + span[1]]]
        bbox = self._geometry.Polygon(bbox)

        # Construct a map containing all ridges for a given point
        all_ridges = collections.defaultdict(list)
        for (p1, p2), (v1, v2) in zip(self.vor.ridge_points, self.vor.ridge_vertices):
            all_ridges[p1].append((p2, v1, v2))
            all_ridges[p2].append((p1, v1, v2))

        new_regions = []
        new_vertices = self.vor.vertices.tolist()
        # Reconstruct infinite regions
        for p1, region in enumerate(self.vor.point_region):
            vertices = self._np.array(self.vor.regions[region])
            if (vertices >= 0).all():
                # doesn't contain infinite regions, can use vertices as it is
                new_regions.append(vertices)
                continue

            # reconstruct a non-finite region
            ridges = all_ridges[p1]
            new_region = vertices[vertices >= 0].tolist()

            for p2, v1, v2 in ridges:
                if v2 < 0:
                    # v2 is always finite, v1 is either finit or inifinite
                    v1, v2 = v2, v1
                if v1 >= 0:
                    # finite ridge: already in the region
                    continue

                # Compute the missing endpoint of an infinite ridge
                t = self.vor.points[p2] - self.vor.points[p1]       # tangent
                t /= self._np.linalg.norm(t)
                n = self._np.array([-t[1], t[0]])                   # normal

                midpoint = self.vor.points[[p1, p2]].mean(axis=0)
                direction = self._np.sign((midpoint - center).dot(n)) * n
                far_point = self.vor.vertices[v2] + direction * radius

                new_region.append(len(new_vertices))
                new_vertices.append(far_point.tolist())

            # sort region counterclockwise
            vs = self._np.asarray([new_vertices[v] for v in new_region])
            c = vs.mean(axis=0)
            angles = self._np.arctan2(vs[:, 1] - c[1], vs[:, 0] - c[0])
            new_region = self._np.array(new_region)[angles.argsort()]

            # finish
            new_regions.append(new_region.tolist())

        new_vertices = self._np.asarray(new_vertices)
        polygons = [new_vertices[r].tolist() for r in new_regions]
        polygons = [self._geometry.Polygon(p) for p in polygons]
        polygons = [p.intersection(bbox) for p in polygons]
        return polygons


class ConvexHull(_Spatial):

    """
    Wrapper for scipy.spatial.ConvexHull

    Parameters
    ----------

    hull : ConvexHull of list of points
    """

    def __init__(self, hull):

        if isinstance(hull, self._spatial.qhull.ConvexHull):
            pass
        else:
            hull = self._spatial.ConvexHull(hull)

        if hull.points.shape[1] != 2:
            raise ValueError("input must be 2 dimentional points or ConvexHull instance")

        self.hull = hull

    def get_polyline(self):
        coordinates = self._get_coordinates()
        return Polyline(positions=coordinates)

    def _get_coordinates(self):

        points = self.hull.points[self.hull.vertices].tolist()
        # append 1st element to last to make loop
        points.append(points[0])
        return points
