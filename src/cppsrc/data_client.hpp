#include <cpr/cpr.h>
#include <iostream>
#include <nlohmann/json.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <string>
#include <unordered_map>
#include <variant>
#include <vector>

class DataClient
{
  public:
    std::string symbol;
    int limit;

    DataClient()
    {
        this->symbol = "btcusd";
        this->limit = 100;
    }


    nlohmann::json _query_api()
    {

        std::string url = "https://api.gemini.com/v1/trades/" + this->symbol;
        cpr::Parameters params = { { "symbol", this->symbol }, { "limit", std::to_string(this->limit) } };

        cpr::Response response = cpr::Get(cpr::Url{ url }, params);
        nlohmann::json json_data = nlohmann::json::parse(response.text);

        return json_data;
    }

    nlohmann::json _parse_message(nlohmann::json message)
    {
        nlohmann::json parsed_message;
        std::vector<std::string> fields = { "type", "amount", "price" };
        for (int i = 0; i < fields.size(); i++) {
            if (message.contains(fields[i])) { parsed_message[0][fields[i]] = message[fields[i]]; }
        }
        return parsed_message[0];
    }

    std::vector<std::unordered_map<std::string, std::string>> get_data()
    {
        nlohmann::json response = this->_query_api();
        std::vector<std::unordered_map<std::string, std::string>> returner;
        for (const auto &item : response) {
            std::unordered_map<std::string, std::string> map;
            for (auto &el : item.items()) {
                map[el.key()] = "";
                for (int i = 1; i < el.value().dump().length() - 1; i++) { map[el.key()] += el.value().dump()[i]; }
            }
            returner.push_back(map);
        }
        return returner;
    }
};