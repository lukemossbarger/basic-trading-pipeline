#pragma once
#include "base_feature.hpp"
#include <array>

using namespace intproj;

class FiveTickVolumeFeature : public BaseFeature
{
    std::array<float, 5> vol_arr;
    int tick;

  public:
    FiveTickVolumeFeature()
    {
        tick = 0;
        for (int i = 0; i < vol_arr.size(); i++) { vol_arr[i] = 0.0; }
    }

    float compute_feature(std::vector<std::tuple<float, float, bool>> data)
    {
        float volume = 0;
        for (int i = 0; i < data.size(); i++) { volume += std::get<1>(data[i]); }
        vol_arr[tick] = volume;
        tick += 1;
        tick %= vol_arr.size();
        volume = 0;
        for (int i = 0; i < vol_arr.size(); i++) { volume += vol_arr[i]; }
        return volume;
    }
};