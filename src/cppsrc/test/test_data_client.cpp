#include "cppsrc/data_client.hpp"
#include <gtest/gtest.h>

TEST(DataClientTests, ParseMessageTest)
{
    DataClient client = DataClient();
    nlohmann::json result = client.get_data();

    for (int i = 0; i < result.size(); i++) {
        EXPECT_TRUE(result[i]["type"] == "sell" || result[i]["type"] == "buy");
        EXPECT_TRUE(result[i]["amount"] > 0);
        EXPECT_TRUE(result[i]["price"] > 0);
    }
}
