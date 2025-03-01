#include "data_client.hpp"
#include "five_tick_sum_feature.hpp"
#include "num_trades_feature.hpp"
#include "percent_buy_feature.hpp"
#include "percent_sell_feature.hpp"
#include <iostream>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

int main()
{
    std::cout << "hello\n";
}

int add(int a, int b)
{
    return a + b;
}

PYBIND11_MODULE(intern, m)
{
    pybind11::class_<BaseFeature>(m, "BaseFeature").def("compute_feature", &BaseFeature::compute_feature);

    pybind11::class_<NTradesFeature>(m, "NTradesFeature")
      .def(pybind11::init<>())
      .def("compute_feature", &NTradesFeature::compute_feature);

    pybind11::class_<PercentBuyFeature>(m, "PercentBuyFeature")
      .def(pybind11::init<>())
      .def("compute_feature", &PercentBuyFeature::compute_feature);

    pybind11::class_<PercentSellFeature>(m, "PercentSellFeature")
      .def(pybind11::init<>())
      .def("compute_feature", &PercentSellFeature::compute_feature);

    pybind11::class_<FiveTickVolumeFeature>(m, "FiveTickVolumeFeature")
      .def(pybind11::init<>())
      .def("compute_feature", &FiveTickVolumeFeature::compute_feature);

    pybind11::class_<DataClient>(m, "DataClient")
      .def(pybind11::init<>())
      .def("_query_api", &DataClient::_query_api)
      .def("_parse_message", &DataClient::_parse_message)
      .def("get_data", &DataClient::get_data);

    m.def("add", &add, "Adds two numbers");
}
