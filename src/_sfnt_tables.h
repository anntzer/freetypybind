#pragma once

#include <array>
#include <map>

namespace matplotlib::ft2::detail {

// conda's clang apparently doesn't like std::string here.
extern std::array<char const*, 7> const tt_platforms;
extern std::array<char const*, 150> const tt_mac_langids;
extern std::map<uint32_t, char const*> const tt_ms_langids;
extern std::array<char const*, 26> const tt_name_ids;

}
