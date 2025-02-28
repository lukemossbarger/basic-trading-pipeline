#pragma once
#include "base_feature.hpp"

using namespace intproj;

class NTradesFeature : public BaseFeature
{

  public:
    NTradesFeature() {}

    float compute_feature(std::vector<std::tuple<float, float, bool>> data)
    {
        return data.size();
    }
};