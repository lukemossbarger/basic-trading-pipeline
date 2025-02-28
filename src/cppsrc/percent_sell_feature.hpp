#pragma once
#include "base_feature.hpp"

using namespace intproj;

class PercentSellFeature : public BaseFeature
{

  public:
    PercentSellFeature() {}

    float compute_feature(std::vector<std::tuple<float, float, bool>> data)
    {
        float sells = 0;
        for (int i = 0; i < data.size(); i++) { sells += !std::get<2>(data[i]); }
        if (!data.size()) { return 0; }
        return sells / data.size();
    }
};