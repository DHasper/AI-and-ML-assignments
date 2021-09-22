// Copyright 2021 RDW
#ifndef INCLUDE_UTILITIES_MATH_HPP_
#define INCLUDE_UTILITIES_MATH_HPP_

#include <dw/core/Types.h>
#include <cstdint>

namespace math {
const double PI = 3.14159265358979323846;

/**
 * value has to be in the range (r1Min, r1Max) and will be mapped to the range (r2Min, r2Max)
 * e.g. value = 0.5, r1Min = 0, r1Max = 1, r2Min = 0, r2Max = 100
 *      returns 50
 *
 * @param value
 * @param r1Min
 * @param r1Max
 * @param r2Min
 * @param r2Max
 * @return
 */
float linearInterpolation(float value, float r1Min, float r1Max, float r2Min, float r2Max);

/**
 * Cast unsigned 32-bit integer to float utilizing memcpy
 *
 * @param inputFloat
 * @return
 */
uint32_t floatToUInt32(float inputFloat);

/**
 * Returns the euclidean distance between two vectors
 *
 * @param p1
 * @param p2
 * @return
 */
float32_t euclidDist(dwVector2f p1, dwVector2f p2);

/**
 * Approximate line length with the euclidean distance of the "begin to middle" segment
 * added to the euclidean distance of the "middle to end" segment
 *
 * Size has to be > 1
 *
 * @param points
 * @param size
 * @return
 */
float32_t approxLineLength(const dwVector2f* points, uint32_t size);

/**
 * Returns the closest vector from array
 *
 * @param pos
 * @param vectors
 * @param size
 * @return
 */
dwVector2f* closestVector(dwVector2f pos, dwVector2f* vectors, int32_t size);

/**
 * Returns a vector between two points
 *
 * @param p1
 * @param p2
 * @return
 */
dwVector2f middleVector(dwVector2f p1, dwVector2f p2);

/**
 * Returns a vector given a position between two points
 * e.g. p1(2, 2), p2(4, 4), pos(0.5) = return(3, 3)
 *
 * @param p1
 * @param p2
 * @param pos
 * @return
 */
dwVector2f middleVector(dwVector2f p1, dwVector2f p2, float32_t pos);

/**
 * Returns a vector following two line having a specific length form p2
 * eg: p1(1, 1), p2(2, 2), length(1) = return(3, 3)
 *
 * @param p1
 * @param p2
 * @param length
 * @return
 */
dwVector2f extendVectorLine(dwVector2f p1, dwVector2f p2, float32_t length);

/**
 * Calculates the orientation given three vectors.
 * It does so by calculating the difference in slopes between two lines (p1, q2) and (q1, p2).
 * Positive output is clockwise, negative output is anti-clockwise, 0 is co-linear.
 * source: https://www.tutorialspoint.com/Check-if-two-line-segments-intersect
 *
 * @param p1
 * @param q1
 * @param p2
 * @return 0 = co-linear, 1 = clockwise, 2 = anti-clockwise
 */
int orientation(dwVector2f* p1, dwVector2f* q1, dwVector2f* p2);

/**
 * Calculates if point p2 is on line (p1,q1)
 * source: https://www.tutorialspoint.com/Check-if-two-line-segments-intersect
 *
 * @param p1
 * @param q1
 * @param p2
 * @return true if p2 is on line (p1,q1)
 */
bool onLine(dwVector2f* p1, dwVector2f* q1, dwVector2f* p2);

/**
 * Checks if line (p1,q1) intersects line (p2,q2)
 *
 * source: https://www.tutorialspoint.com/Check-if-two-line-segments-intersect
 *
 * @param p1
 * @param q1
 * @param p2
 * @param q2
 * @return true if lines intersect
 */
bool intersect(dwVector2f* p1, dwVector2f* q1, dwVector2f* p2, dwVector2f* q2);

bool pointInBoundary(dwVector2f* point, dwVector2f* boundary, const uint32_t size);
}  // namespace math

#endif  // INCLUDE_UTILITIES_MATH_HPP_
