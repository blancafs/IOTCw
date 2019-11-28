//#include "Vec3f.h"
//#include <mbed.h>
//
//
//
//
//Serial pc(USBTX, USBRX);
//
//Vec3f::Vec3f(float x, float y, float z) {
//    set(x, y, z);
//}
//
//Vec3f::Vec3f(){
//}
//
//Vec3f::Vec3f(Vec3f &arg) {
//    set(arg);
//}
//
//void Vec3f::set(Vec3f *arg) {
//    set(arg->x_Conflict, arg->y_Conflict, arg->z_Conflict);
//}
//
//void Vec3f::set(float x, float y, float z) {
//    this->x_Conflict = x;
//    this->y_Conflict = y;
//    this->z_Conflict = z;
//}
//
//void Vec3f::set(int i, float val) {
//    switch (i) {
//        case 0: x_Conflict = val;   break;
//        case 1: y_Conflict = val;   break;
//        case 2: z_Conflict = val;   break;
//        default: x_Conflict = x_Conflict;
//    }
//}
//
//float Vec3f::get(int i) {
//    switch (i) {
//        case 0: return x_Conflict;
//        case 1: return y_Conflict;
//        case 2: return z_Conflict;
//        default: return x_Conflict;
//    }
//}
//
//float Vec3f::x() {
//    return x_Conflict;
//}
//
//float Vec3f::y() {
//    return y_Conflict;
//}
//
//float Vec3f::z() {
//    return z_Conflict;
//}
//
//void Vec3f::setX(float x)   {
//    this->x_Conflict = x;
//}
//
//void Vec3f::setY(float y)   {
//    this->y_Conflict = y;
//}
//
//void Vec3f::setZ(float z)   {
//    this->z_Conflict = z;
//}
//
//float Vec3f::dot(Vec3f *v)    {
//    float result = x_Conflict * v->x_Conflict + y_Conflict * v->y_Conflict + z_Conflict * v->z_Conflict;
//    return result;
//}
//
//float Vec3f::length()   {
//    return static_cast<float>(std::sqrt(lengthSquared()));
//}
//
//float Vec3f::lengthSquared()    {
//    float result = this->dot(this);
//    return result;
//}
//
//void Vec3f::normalize() {
//    float len = length();
//    if (len == 0.0f)
//    {
//        return;
//    }
//    scale(1.0f / len);
//}
//
//Vec3f Vec3f::times(float val) {
//    Vec3f *tmp = new Vec3f(this);
//    tmp->scale(val);
//    return tmp;
//}
//
//void Vec3f::scale(float val) {
//    x_Conflict *= val;
//    y_Conflict *= val;
//    z_Conflict *= val;
//}
//
//Vec3f *Vec3f::plus(Vec3f *arg) {
//    Vec3f *tmp = new Vec3f();
//    tmp->add(this, arg);
//    return tmp;
//}
//
//void Vec3f::add(Vec3f *b) {
//    add(this, b);
//}
//
//void Vec3f::add(Vec3f *a, Vec3f *b){
//    x_Conflict = a->x_Conflict + b->x_Conflict;
//    y_Conflict = a->y_Conflict + b->y_Conflict;
//    z_Conflict = a->z_Conflict + b->z_Conflict;
//}
//
//Vec3f Vec3f::addScaled(float s, Vec3f *arg) {
//    Vec3f *tmp = new Vec3f();
//    tmp->addScaled(this, s, arg);
//    return tmp;
//}
//
//void Vec3f::addScaled(Vec3f *a, float s, Vec3f *b) {
//    x_Conflict = a->x_Conflict + s * b->x_Conflict;
//    y_Conflict = a->y_Conflict + s * b->y_Conflict;
//    z_Conflict = a->z_Conflict + s * b->z_Conflict;
//}
//
//Vec3f Vec3f::minus(Vec3f *arg) {
//    Vec3f *tmp = new Vec3f();
//    tmp->sub(this, arg);
//    return tmp;
//}
//
//void Vec3f::sub(Vec3f *b)   {
//    sub(this, b);
//}
//
//void Vec3f::sub(Vec3f *a, Vec3f *b) {
//    x_Conflict = a->x_Conflict - b->x_Conflict;
//    y_Conflict = a->y_Conflict - b->y_Conflict;
//    z_Conflict = a->z_Conflict - b->z_Conflict;
//}
