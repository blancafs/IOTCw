#pragma once

#include <string>
#include <cmath>
#include <stdexcept>

namespace com::specknet::orientandroid
{

	/** 3-element single-precision vector */

	class Vec3f
	{
	public:
		static const Vec3f X_AXIS;
		static const Vec3f Y_AXIS;
		static const Vec3f Z_AXIS;
		static const Vec3f NEG_X_AXIS;
		static const Vec3f NEG_Y_AXIS;
		static const Vec3f NEG_Z_AXIS;

	private:
		float x_Conflict = 0;
		float y_Conflict = 0;
		float z_Conflict = 0;

	public:
		Vec3f();

		Vec3f(const Vec3f &arg);

		Vec3f(float x, float y, float z);

		virtual void set(Vec3f *arg);

		virtual void set(float x, float y, float z);

		/** Sets the ith component, 0 <= i < 3 */
		virtual void set(int i, float val);

		/** Gets the ith component, 0 <= i < 3 */
		virtual float get(int i);

		virtual float x();
		virtual float y();
		virtual float z();

		virtual void setX(float x);
		virtual void setY(float y);
		virtual void setZ(float z);

		virtual float dot(Vec3f *arg);

		virtual float length();

		virtual float lengthSquared();

		virtual void normalize();

		/** Returns this * val; creates new vector */
		virtual Vec3f *times(float val);

		/** this = this * val */
		virtual void scale(float val);

		/** Returns this + arg; creates new vector */
		virtual Vec3f *plus(Vec3f *arg);

		/** this = this + b */
		virtual void add(Vec3f *b);

		/** this = a + b */
		virtual void add(Vec3f *a, Vec3f *b);

		/** Returns this + s * arg; creates new vector */
		virtual Vec3f *addScaled(float s, Vec3f *arg);

		/** this = a + s * b */
		virtual void addScaled(Vec3f *a, float s, Vec3f *b);

		/** Returns this - arg; creates new vector */
		virtual Vec3f *minus(Vec3f *arg);

		/** this = this - b */
		virtual void sub(Vec3f *b);

		/** this = a - b */
		virtual void sub(Vec3f *a, Vec3f *b);

		/** Returns this cross arg; creates new vector */
		virtual Vec3f *cross(Vec3f *arg);

		/** this = a cross b. NOTE: "this" must be a different vector than
		 both a and b. */
		virtual void cross(Vec3f *a, Vec3f *b);

		/** Sets each component of this vector to the product of the
		 component with the corresponding component of the argument
		 vector. */
		virtual void componentMul(Vec3f *arg);

		virtual std::wstring toString();
	};

}
