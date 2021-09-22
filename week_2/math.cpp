// Copyright 2021 RDW
#include <Utilities/math.hpp>
#include <cstring>
#include <cmath>
#include <limits>
#include <iostream>

float math::linearInterpolation(float value,
                                        float r1Min,
                                        float r1Max,
                                        float r2Min,
                                        float r2Max) {
    return (value - r1Min) * (r2Max - r2Min) / (r1Max - r1Min) + r2Min;
}

uint32_t math::floatToUInt32(float inputFloat) {
    uint32_t output;
    memcpy(&output, &inputFloat, sizeof(output));
    return output;
}

float32_t math::euclidDist(dwVector2f p1, dwVector2f p2) {
    return std::sqrt(std::pow(p1.x - p2.x, 2) + std::pow(p1.y - p2.y, 2));
}

float32_t math::approxLineLength(const dwVector2f* points, uint32_t size) {
    return math::euclidDist(points[0], points[size/2]) +
           math::euclidDist(points[size/2], points[size-1]);
}

dwVector2f* math::closestVector(dwVector2f pos, dwVector2f* vectors, int32_t size) {
    dwVector2f* closest_point;
    float32_t closest_length = -1;

    for (int32_t i = 0; i < size; i++) {
        float32_t cur_length = euclidDist(pos, vectors[i]);

        if (cur_length < closest_length || closest_length == -1) {
            closest_point = &vectors[i];
            closest_length = cur_length;
        }

        if (cur_length == 0) {
            break;
        }
    }

    return closest_point;
}

dwVector2f math::middleVector(dwVector2f p1, dwVector2f p2) {
    dwVector2f middle_vector;

    middle_vector.x = (p1.x + p2.x) / 2.0f;
    middle_vector.y = (p1.y + p2.y) / 2.0f;

    return middle_vector;
}

dwVector2f math::middleVector(dwVector2f p1, dwVector2f p2, float32_t pos) {
    if (pos == 0) {
        return p1;
    }

    dwVector2f middle_vector;
    middle_vector.x = p1.x + pos * (p2.x - p1.x);
    middle_vector.y = p1.y + pos * (p2.y - p1.y);

    return middle_vector;
}

dwVector2f math::extendVectorLine(dwVector2f p1, dwVector2f p2, float32_t length) {
    if (length == 0) {
        return p2;
    }

    dwVector2f p3;

    float32_t lenAB = euclidDist(p1, p2);
    p3.x = p2.x + (p2.x - p1.x) / lenAB * length;
    p3.y = p2.y + (p2.y - p1.y) / lenAB * length;

    return p3;
}

int math::orientation(dwVector2f* p1, dwVector2f* q1, dwVector2f* p2) {
    float o = (q1->y-p1->y) * (p2->x-q1->x) - (q1->x-p1->x) * (p2->y-q1->y);

    if (o == 0) return 0;
    else if (o < 0) return 2;
    return 1;
}

bool math::onLine(dwVector2f* p1, dwVector2f* q1, dwVector2f* p2) {
    if (p2->x <= std::fmax(p1->x, q1->x) && p2->x <= std::fmin(p1->x, q1->x) &&
        (p2->y <= std::fmax(p1->y, q1->y) && p2->y <= std::fmin(p1->y, q1->y)))
        return true;

    return false;
}

bool math::intersect(dwVector2f* p1, dwVector2f* q1, dwVector2f* p2, dwVector2f* q2) {
    int o1 = orientation(p1, q1, p2);
    int o2 = orientation(p1, q1, q2);
    int o3 = orientation(p2, q2, p1);
    int o4 = orientation(p2, q2, q1);

    if (o1 != o2 && o3 != o4) return true;

    if (o1 == 0 && onLine(p1, q1, p2)) return true;
    if (o2 == 0 && onLine(p1, q1, q2)) return true;
    if (o3 == 0 && onLine(p2, q2, p1)) return true;
    if (o4 == 0 && onLine(p2, q2, q1)) return true;

    return false;
}

bool math::pointInBoundary(dwVector2f* point, dwVector2f* boundary, const uint32_t size) {
    dwVector2f rayPoint = {std::numeric_limits<float32_t>::max(), point->y};

    int intersectCount = 0;
    for (int pointIndex = 0; pointIndex < size-1; pointIndex++) {
        if (intersect(point, &rayPoint, &boundary[pointIndex], &boundary[pointIndex+1]))
            intersectCount++;
    }

    return intersectCount % 2 == 0 ? false : true;
}
