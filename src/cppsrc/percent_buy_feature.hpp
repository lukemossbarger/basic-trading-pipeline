#pragma once
#include "base_feature.hpp"

using namespace intproj;

class PercentBuyFeature : public BaseFeature
{

  public:// tuple is <price, volume, buy> where buy == false means it is a sell
    PercentBuyFeature() {}

    float compute_feature(std::vector<std::tuple<float, float, bool>> data)
    {
        float buys = 0;
        for (int i = 0; i < data.size(); i++) { buys += std::get<2>(data[i]); }
        if (!data.size()) { return 0; }
        return buys / data.size();
    }
};