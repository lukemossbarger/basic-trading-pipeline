#include "cppsrc/percent_sell_feature.hpp"
#include "gtest/gtest.h"

TEST(FeatureTests, PctSellTest)
{
    PercentSellFeature psf = PercentSellFeature();
    EXPECT_EQ(psf.compute_feature({ { 1, 1, false } }), 1);
    EXPECT_EQ(psf.compute_feature({ { 1, 1, false }, { 1, 1, true } }), 0.5);
    EXPECT_NEAR(psf.compute_feature({ { 1, 1, false }, { 1, 1, true }, { 1, 2, false } }), 0.666666667, 1e-6);
}
