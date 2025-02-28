#include "cppsrc/num_trades_feature.hpp"
#include "gtest/gtest.h"

TEST(FeatureTests, NTradesTest)
{
    NTradesFeature ntf = NTradesFeature();
    EXPECT_EQ(ntf.compute_feature({ { 1, 1, false } }), 1);
    EXPECT_EQ(ntf.compute_feature({ { 2, 1, false }, { 2, 2, true } }), 2);
}
