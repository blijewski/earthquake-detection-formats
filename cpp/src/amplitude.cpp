#include <amplitude.h>

#include <string>
#include <limits>
#include <vector>

// JSON Keys
#define AMPLITUDE_KEY "Amplitude"
#define PERIOD_KEY "Period"
#define SNR_KEY "SNR"

namespace detectionformats {
amplitude::amplitude() {
	ampvalue = std::numeric_limits<double>::quiet_NaN();
	period = std::numeric_limits<double>::quiet_NaN();
	snr = std::numeric_limits<double>::quiet_NaN();
}

amplitude::amplitude(double newampvalue, double newperiod, double newsnr) {
	ampvalue = newampvalue;
	period = newperiod;
	snr = newsnr;
}

amplitude::amplitude(rapidjson::Value &json) {
	// optional values
	// ampvalue
	if ((json.HasMember(AMPLITUDE_KEY) == true)
			&& (json[AMPLITUDE_KEY].IsNumber() == true)
			&& (json[AMPLITUDE_KEY].IsDouble() == true))
		ampvalue = json[AMPLITUDE_KEY].GetDouble();
	else
		ampvalue = std::numeric_limits<double>::quiet_NaN();

	// period
	if ((json.HasMember(PERIOD_KEY) == true)
			&& (json[PERIOD_KEY].IsNumber() == true)
			&& (json[PERIOD_KEY].IsDouble() == true))
		period = json[PERIOD_KEY].GetDouble();
	else
		period = std::numeric_limits<double>::quiet_NaN();

	// snr
	if ((json.HasMember(SNR_KEY) == true) && (json[SNR_KEY].IsNumber() == true)
			&& (json[SNR_KEY].IsDouble() == true))
		snr = json[SNR_KEY].GetDouble();
	else
		snr = std::numeric_limits<double>::quiet_NaN();
}

amplitude::amplitude(const amplitude & newamplitude) {
	ampvalue = newamplitude.ampvalue;
	period = newamplitude.period;
	snr = newamplitude.snr;
}

amplitude::~amplitude() {
}

rapidjson::Value & amplitude::tojson(
		rapidjson::Value &json,
		rapidjson::MemoryPoolAllocator<rapidjson::CrtAllocator> &allocator) {
	json.SetObject();

	// optional values
	// ampvalue
	if (std::isnan(ampvalue) != true)
		json.AddMember(AMPLITUDE_KEY, ampvalue, allocator);

	// period
	if (std::isnan(period) != true)
		json.AddMember(PERIOD_KEY, period, allocator);

	// snr
	if (std::isnan(snr) != true)
		json.AddMember(SNR_KEY, snr, allocator);

	return (json);
}

std::vector<std::string> amplitude::geterrors() {
	std::vector<std::string> errorlist;

	// optional data
	// period
	if (std::isnan(period) != true) {
		if (period < 0) {
			errorlist.push_back("Invalid Period in Amplitude class.");
		}
	}

	// SNR
	if (std::isnan(snr) != true) {
		// Limit SNR to between 0 and 10 digits after the decimal point
		if ((snr < 0) || (snr > 9999999999.999)) {
			errorlist.push_back(
					"SNR in Amplitude Class is not in the valid range of 0 to "
					"9999999999.999");
		}
	}

	return (errorlist);
}

bool amplitude::isempty() {
	if (std::isnan(ampvalue) != true)
		return (false);
	if (std::isnan(period) != true)
		return (false);
	if (std::isnan(snr) != true)
		return (false);

	return (true);
}
}  // namespace detectionformats
