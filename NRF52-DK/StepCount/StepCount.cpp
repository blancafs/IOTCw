
#include "StepCount.h"
#include <cmath>
#include <vector>

    // Initialises all values
    StepCount::StepCount(){
      mean = 0;
      stdDev = 0;
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
      filtered = std::vector<double>(); // holds mags of vals
      // Private
      //enum class State {PEAK, VALLEY, INIT, INTMD};
      staten = State::INIT;
      count = 0; 
      windowSize = 5;
      windowStdSize = 10;
      accelList = std::vector<std::vector<float>>();
      temp = std::vector<std::vector<float>>();
      peakList = std::vector<double>();
      valleyList = std::vector<double>();
}

    // Gets mean of given list
    float StepCount::getMean(std::vector<double> list) {
      float sum = 0;
      for (int i = 0; i < list.size(); i++)    {
        sum += list.at(i);
      }
      sum = sum / (list.size());
      return sum;
}

    // Gets standard deviation of a given list
    float StepCount::getStdDev(std::vector<double> list) {
      double newmean = getMean(list);
      double sum = 0;
      for (int i = 0; i < list.size(); i++) {
        sum += (list.at(i) - newmean) * (list.at(i) - newmean);
      }
      sum = sum / (list.size());
      sum = std::sqrt(sum);
      float ret = static_cast<float>(sum);
      return ret;
    }

    // Classifies state
    State StepCount::detectCandidate(double anmin, double an, double anplus) {
      State statec = State::INTMD; // Assuming norm is intermediate
      if (an>fmax(anmin, fmax(anplus, mean + (stdDev / alpha)))) {
        statec = State::PEAK;
      }
      else if (an < fmin(anmin, fmin(anplus, mean - (stdDev / alpha))))   {
          statec = State::VALLEY;
      }
      return statec;
    }

    // Updates peak values
    void StepCount::updatePeak(double an, int n) {
      peakList.push_back(static_cast<double>(n));
      std::vector<double> temp = std::vector<double>();
      for (int i = fmax(0, peakList.size() - windowSize); i < peakList.size() - 1; i++) {
          temp.push_back(peakList.at(i + 1) - peakList.at(i));
      }
      up = getMean(temp);
      stdp = getStdDev(temp);
      np = n;
      ap = an;
      Thp = up - (stdp/beta);
    }

    // Updates valley values
    void StepCount::updateValley(double an, int n) {
      valleyList.push_back(static_cast<double>(n));
      std::vector<double> temp = std::vector<double>(); // for window
      for (int i = fmax(0, valleyList.size() - windowSize); i < valleyList.size() - 1; i++) {
        temp.push_back(valleyList.at(i + 1) - valleyList.at(i));
      }
      uv = getMean(temp);
      stdv = getStdDev(temp);
      nv = n;
      av = an;
      Thv = uv - (stdv / beta);
    }

    // Classifies step and updates peaks and valleys
    int StepCount::stepDetection(float accel_x, float accel_y, float accel_z) {
      std::vector<float> accelVector(3);
      accelVector[0] = accel_x;
      accelVector[1] = accel_y;
      accelVector[2] = accel_z;
      accelList.push_back(accelVector);
      double mag = std::sqrt(accel_x*accel_x+accel_y*accel_y+accel_z*accel_z);
      // camping and cutting
      if (mag>1.4){mag =1.4;}
      if (mag < 0.8){mag=0.8;}
      filtered.push_back(mag);

      int n = filtered.size() - 2;
      if (filtered.size() < windowSize) {
        return count;
      }
      double anmin = filtered.at(n-1);
      double an = filtered.at(n);
      double anplus = filtered.at(n + 1);
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
        std::vector<double> temp = std::vector<double>();
        for (int i = fmax(0, accelList.size() - windowStdSize); i < accelList.size(); i++) {temp.push_back(filtered.at(i));}
        stdDev = getStdDev(temp);
        if (std::isnan(Thp)) { Thp = 0;}
        if (std::isnan(Thv)) { Thv = 0;}
        if (Thp<0) { Thp = 0;}
        if (Thv<0) { Thv = 0;}
      }
      return count;
    }
