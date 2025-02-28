#include "base_feature.hpp"

using namespace intproj;

class PercentBuyFeature : public BaseFeature
{

  public:// tuple is <price, volume, buy> where buy == false means it is a sell
    PercentBuyFeature() {}

    float compute_feature(std::vector<std::tuple<float, float, bool>> data)
    {
        float total = 0;
        float buys = 0;
        for (int i = 0; i < data.size(); i++) {
            total += std::get<1>(data[i]);
            if (std::get<2>(data[i])) { buys += std::get<1>(data[i]); }
        }
        if (!total) { return 0; }
        return buys / total;
    }
};