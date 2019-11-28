//#include <string>
//#include <cmath>
//#include <stdexcept>
//#pragma once
//
///** 3-element single-precision vector */
//
//class Vec3f {
//    private:
//        float x_Conflict = 0;
//        float y_Conflict = 0;
//        float z_Conflict = 0;
//    
//    public:
//        Vec3f();
//    
//        Vec3f(Vec3f &arg);
//    
//        Vec3f(float x, float y, float z);
//    
//        void set(Vec3f *arg);
//    
//        void set(float x, float y, float z);
//    
//        /** Sets the ith component, 0 <= i < 3 */
//        void set(int i, float val);
//    
//        /** Gets the ith component, 0 <= i < 3 */
//        float get(int i);
//    
//        float x();
//        float y();
//        float z();
//    
//        void setX(float x);
//        void setY(float y);
//        void setZ(float z);
//    
//        float dot(Vec3f *arg);
//    
//        float length();
//    
//        float lengthSquared();
//    
//        void normalize();
//    
//        /** Returns this * val; creates new vector */
//        Vec3f times(float val);
//    
//        /** this = this * val */
//        void scale(float val);
//    
//        /** Returns this + arg; creates new vector */
//        Vec3f plus(Vec3f *arg);
//    
//        /** this = this + b */
//        void add(Vec3f *b);
//    
//        /** this = a + b */
//        void add(Vec3f *a, Vec3f *b);
//    
//        /** Returns this + s * arg; creates new vector */
//        Vec3f *addScaled(float s, Vec3f *arg);
//    
//        /** this = a + s * b */
//        void addScaled(Vec3f *a, float s, Vec3f *b);
//    
//        /** Returns this - arg; creates new vector */
//        Vec3f minus(Vec3f *arg);
//    
//        /** this = this - b */
//        void sub(Vec3f *b);
//    
//        /** this = a - b */
//        void sub(Vec3f *a, Vec3f *b);
//    
//        /** Returns this cross arg; creates new vector */
//        Vec3f cross(Vec3f *arg);
//    
//        /** this = a cross b. NOTE: "this" must be a different vector than
//         both a and b. */
//        void cross(Vec3f *a, Vec3f *b);
//    
//        /** Sets each component of this vector to the product of the
//         component with the corresponding component of the argument
//         vector. */
//        void componentMul(Vec3f *arg);
//};
//
