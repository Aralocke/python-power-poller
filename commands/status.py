def PrettyDuration(seconds, values=2):
    table = [('Weeks', 604800), ('Days', 86400), ('Hours', 3600),
             ('Minutes', 60), ('Seconds', 0)]
    if seconds <= 0:
        return 'N/A'
    results = []
    for (string, value) in table:
        if len(results) == values:
            break
        count = int(seconds / value)
        if count == 0:
            continue
        seconds -= (count * value)
        results.append('{} {}'.format(count, string))
    return ' '.join(results)


def SignalStrength(value):
    """
    Returns a string indicating the signal strength of the WiFi signal
    in human-readable terms.

    Based on the table from:
    https://www.metageek.com/training/resources/understanding-rssi.html

    :param value: WiFI signal strength RSSI value
    :return: String represent signal strength
    """
    if value > -30:
        return 'Excellent'
    if value > -67:
        return 'Very Good'
    if value > -70:
        return 'Good'
    if value > -80:
        return 'Poor'
    if value > -90:
        return 'Weak'
    return 'N/A'

def Status(devices, args):
    for device in devices:
        print('-' * 30)
        print('Device Information')
        print('\tAddress: {}'.format(device.address))
        print('\tAlias: {}'.format(device.GetAlias()))
        print('\tDevice Type: {} ({})'.format(device.GetType(), device.GetTypeString()))
        print('\tDevice Model: {}'.format(device.GetModel()))
        print('\tDevice Identifier: {}'.format(device.GetDeviceIdentifier()))
        print('\tDescription: {}'.format(device.GetDescription()))
        print()

        print('Device State')
        print('\tUptime: {}'.format(PrettyDuration(device.GetUptime())))
        print('\tState: {}'.format('On' if device.IsOn() else 'Off'))

        if device.IsPlug():
            print('\tLED: {}'.format('On' if device.IsLedOn() else 'Off'))
        if device.IsBulb():
            print('\tColor Supported: {}'.format('Yes' if device.IsColorSupported() else 'No'))
            print('\tBrightness Supported: {}'.format('Yes' if device.IsBrightnessSupported() else 'No'))
            if device.IsColorSupported() and device.IsOn():
                print('\tHue: {}'.format(device.GetHue()))
                print('\tSaturation: {}'.format(device.GetSaturation()))
                print('\tBrightness: {}'.format(device.GetBrightness()))
                print('\tTemperature: {}'.format(device.GetTemperature()))
        print()

        if device.HasEmeter():
            print('Electricity Meter')
            emeter = device.GetEmeter()
            print('\tAmperage: {} amps'.format(emeter.GetAmps()))
            print('\tConsumption: {} watts'.format(emeter.GetConsumption()))
            print('\tVoltage: {} volts'.format(emeter.GetVoltage()))
            print('\tDaily Usage (kW/H): {}'.format(emeter.GetUsageToday()))
            print('\tAverage Daily Usage (kW/H): {}'.format(emeter.GetDailyAverage()))
            print('\tMonthly Usage (kW/H): {}'.format(emeter.GetUsageMonth()))
            print('\tAverage Monthly Usage (kW/H): {}'.format(emeter.GetMonthlyAverage()))
            print()

        print('Version Information')
        print('\tSoftware Version: {}'.format(device.GetSoftwareVersion()))
        print('\tHardware Version: {}'.format(device.GetHardwareVersion()))
        print()

        print('Network Status')
        print('\tMAC Address: {}'.format(device.GetMacAddress()))
        strength = device.GetSignalStrength()
        print('\tWiFi Strength: {} ({})'.format(SignalStrength(strength), strength))
        print()
