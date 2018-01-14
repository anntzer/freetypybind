#pragma once

#include <array>
#include <map>

namespace matplotlib::ft2::detail {

extern std::array<std::string, 7> const tt_platforms;
extern std::array<std::string, 150> const tt_mac_langids;
extern std::map<uint32_t, std::string> const tt_ms_langids;
extern std::array<std::string, 26> const tt_name_ids;

}
