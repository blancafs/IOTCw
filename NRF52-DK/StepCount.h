#include "Vec3f.h"

class StepCount {

	public:
		enum State {PEAK, VALLEY, INIT, INTMD};
		double mean; // acceleration mean
		float std; // deviation of magnitude of accels
		float alpha;
		int np; // index for last peak
		int nv; // index for recent valley
		float Thp; // adaptive peak threshold
		float Thv; // adaptive valley threshold
		double ap;
		double av;
		float stdp; // deviation of peaks
		float stdv;
		float beta;
		float up;
		float uv;
    std::vector<double> *filtered; // holds mags of vals

	private:
		State staten;
		int count;
		int windowSize;
		int windowStdSize;
		std::vector<Vec3f> *accelList; // will hold accels
		std::vector<Vec3f> *temp; // do we need?
		std::vector<double> *peakList; // tracks peaks
		std::vector<double> *valleyList; // tracks valleys
		std::vector<float> *accel_xs;

	public:
    StepCount(); // Initialises all values
    float getMean(std::vector<double> *list);// Gets mean of given list
    float getStdDev(std::vector<double> *list); // Gets standard deviation of a given list
    State detectCandidate(double anmin, double an, double anplus);   // Classifies state
    void updatePeak(double an, int n); // Updates peak values
    void updateValley(double an, int n); // Updates valley values
    int stepDetection(std::vector<double> magList); // Classifies step and updates peaks and valleys
};
