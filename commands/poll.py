from monitor.lib import ConversionFailure, Metric, Result
from tplink.discover import LoadDevice
from tplink.exceptions import ConnectionError
from tplink.utils import IsValidIPv4


def ProcessDevice(pipeline, name, config, logger=None):
    address = config['address']
    if not IsValidIPv4(address):
        if logger:
            logger.error('Invalid device configuration: {}'.format(name))
        return False

    try:
        device = LoadDevice(address, logger=logger)
    except ConnectionError as e:
        if logger:
            logger.warning('Failed to connect to: {}'.format(address))
        return True

    if not device.HasEmeter():
        if logger:
            logger.warning("Device '{}' does not support electronic metering".format(
                device.GetAlias()))
        return False

    emeter = device.GetEmeter()
    try:
        result = emeter.GetRealtime(cache=False)
    except ConnectionError:
        if logger:
            logger.warning('Failed to get realtime data for: {}'.format(address))
        return True

    if 'err_code' not in result or result['err_code'] != 0:
        if logger:
            logger.error("Failed to load device '{}' emeter data".format(device.GetAlias()))
        return False

    tags = {'device': config['device']}
    tags.update(config.get('tags', {}))

    metric = Metric(name, 'emeter', tags=tags)
    measurements = config['measurements'][metric.measurement]

    for key, value in result.items():
        if key not in measurements:
            continue
        metric.AddField(key, value)

    try:
        pipeline(metric)
    except ConversionFailure:
        pass

    return True


def Poll(config, logger, pipeline):
    """

    :param config:
    :param logger:
    :param pipeline:
    :return:
    """
    success = True
    for device, cfg in config.items():
        try:
            ProcessDevice(pipeline, device, cfg, logger=logger)
        except ConnectionError as e:
            if logger:
                logger.error("Failed to connect to '{}': {}".format(device, e.message))

    return Result.SUCCESS if success else Result.FAILURE
