#include "cppsrc/percent_buy_feature.hpp"
#include "gtest/gtest.h"

TEST(FeatureTests, PctBuyTest)
{
    PercentBuyFeature ptf = PercentBuyFeature();
    EXPECT_EQ(ptf.compute_feature({ { 1, 1, false } }), 0);
    EXPECT_EQ(ptf.compute_feature({ { 1, 1, false }, { 1, 1, true } }), 0.5);
    EXPECT_EQ(ptf.compute_feature({ { 1, 1, true } }), 1);
}
