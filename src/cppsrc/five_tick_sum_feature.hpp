#include "base_feature.hpp"

using namespace intproj;

class FiveTickVolumeFeature : public BaseFeature
{
    float *vol_arr;
    int num_ticks;
    int tick;

  public:// tuple is <price, volume, buy> where buy == false means it is a sell
    FiveTickVolumeFeature()
    {
        num_ticks = 5;
        tick = 0;
        vol_arr = new float[num_ticks];
        for (int i = 0; i < num_ticks; i++) { vol_arr[i] = 0.0; }
    }

    float compute_feature(std::vector<std::tuple<float, float, bool>> data)
    {
        float volume = 0;
        for (int i = 0; i < data.size(); i++) { volume += std::get<1>(data[i]); }
        vol_arr[tick] = volume;
        tick += 1;
        tick %= num_ticks;
        volume = 0;
        for (int i = 0; i < num_ticks; i++) { volume += vol_arr[i]; }
        return volume;
    }
};