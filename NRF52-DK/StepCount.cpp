#include "Vec3f.h"
#include "countsteps.h"

    // Initialises all values
    StepCount::StepCount(){
  mean = 0;
  std = 0;
  alpha =  3.0f;
  np = 0;
  nv = 0;
  Thp = 0; // adaptive peak threshold
  Thv = 0; // adaptive valley threshold
  ap = 0;
  av = 0;
  stdp = 0; // deviation of peaks
  stdv = 0;
  beta = 1.4f;
  up = 0;
  uv = 0;
  std::vector<double> *filtered = std::vector<double>(); // holds mags of vals
  // Private
  State staten = State.INIT;
  int count = 0;
  int windowSize = 5;
  int windowStdSize = 10;
  std::vector<Vec3f> *accelList = std::vector<Vec3f>();
  std::vector<Vec3f> *temp = std::vector<Vec3f>();
  std::vector<double> *peakList = std::vector<double>();
  std::vector<double> *valleyList = std::vector<double>();
  std::vector<float> *accel_xs = std::vector<float>();
}

    // Gets mean of given list
    float StepCount::getMean(std::vector<double> *list) {
  float sum = 0;
  for (int i = 0; i < list->size(); i++)	{
    sum += list->get(i);
  }
  sum = sum / (list->size());
  return sum;
}

    // Gets standard deviation of a given list
    float StepCount::getStdDev(std::vector<double> *list) {
      double newmean = getMean(list);
      double sum = 0;
      for (int i = 0; i < list->size(); i++) {
        sum += (list->get(i) - newmean) * (list->get(i) - newmean);
      }
      sum = sum / (list->size());
      sum = std::sqrt(sum);
      float ret = static_cast<float>(sum);
      return ret;
    }

    // Classifies state
    State StepCount::detectCandidate(double anmin, double an, double anplus) {
      State statec = State::INTMD; // Assuming norm is intermediate
      if (an>max(anmin, max(anplus, mean + (stdDev / alpha)))) {
        statec = State::PEAK;
      }
      else if (an < min(anmin, min(anplus, mean - (stdDev / alpha))))	{
          statec = State::VALLEY;
      }
      return statec;
    }

    // Updates peak values
    void StepCount::updatePeak(double an, int n) {
      peakList->add(static_cast<double>(n));
      std::vector<double> *temp = std::vector<double>();
      for (int i = max(0, peakList->size() - windowSize); i < peakList->size() - 1; i++) {
          temp->add(peakList->get(i + 1) - peakList->get(i));
      }
      up = getMean(temp);
      stdp = getStdDev(temp);
      np = n;
      ap = an;
      Thp = up - (stdp/beta);
    }

    // Updates valley values
    void StepCount::updateValley(double an, int n) {
      valleyList->add(static_cast<double>(n));
      std::vector<double> *temp = std::vector<double>(); // for window
      for (int i = max(0, valleyList->size() - windowSize); i < valleyList->size() - 1; i++) {
        temp->add(valleyList->get(i + 1) - valleyList->get(i));
      }
      uv = getMean(temp);
      stdv = getStdDev(temp);
      nv = n;
      av = an;
      Thv = uv - (stdv / beta);
    }

    // Classifies step and updates peaks and valleys
    int StepCount::stepDetection(std::vector<double> magList) {
      int n = magList->size() - 2;
      if magList->size() < windowSize) {
        return;
      }
      double anmin = magList->get(n-1);
      double an = magList->get(n);
			double anplus = magList->get(n + 1);
			State stateCandidate = detectCandidate(anmin, an, anplus);

      if (stateCandidate==State::PEAK) {
        if (staten==State::INIT) {
          staten = State::PEAK;
          updatePeak(an, n);
          mean = an;
        }
        else if (staten==State::VALLEY && (n-np)>Thp) {
          staten = State::PEAK;
          updatePeak(an, n);
          mean = (ap+av)/2;
        }
        else if (staten==State::PEAK && (n-np)<=Thp && an>ap) {
          updatePeak(an, n);
        }
        else if (stateCandidate==State::VALLEY) {
          if (staten==State::PEAK && (n-nv)>Thv) {
            staten = State::VALLEY;
            updateValley(an, n);
            mean = (ap+av)/2;
            if (stdDev>0.1) {
              count++;
            }
          }
          else if (staten==State::VALLEY && (n-nv)<=Thv && an<av) {
            updateValley(an, n);
          }
        }
        // filling temp with mags in window
        std::vector<double> *temp = std::vector<double>();
        for (int i = max(0, accelList->size() - windowStdSize); i <	accelList->size(); i++) {
  					temp->add(magList->get(i));
  				}
        stdDev = getStdDev(temp);
        if (std::isnan(Thp)) { Thp = 0;}
        if (std::isnan(Thv)) { Thv = 0;}
        if (Thp<0) { Thp = 0;}
        if (Thv<0) { Thv = 0;}
      }
      return count;
    }
