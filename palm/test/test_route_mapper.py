import nose.tools
import numpy
from ..blink_parameter_set import SingleDarkParameterSet
from ..rate_fcn import rate_from_rate_id


EPSILON = 0.01

def compute_fermi_log_ka(time, T, tf):
    numerator = numpy.exp(-(time - tf) / T)
    denominator = ((1 + numerator) * numpy.log(1 + numerator)) * T
    if denominator < 1e-10:
        ka = 0.2
    else:
        ka = numerator/denominator
    return numpy.log10(ka)

@nose.tools.istest
def fermi_ka_at_time_zero_matches_expected_value():
    params = SingleDarkParameterSet()
    T = 5.0 # seconds
    tf = 192.0 # seconds
    params.set_parameter('fermi_T', T)
    params.set_parameter('fermi_tf', tf)
    ka_at_time_zero = rate_from_rate_id(
                        'ka', 0.0, params, fermi_activation=True)
    log_ka_at_time_zero = numpy.log10(ka_at_time_zero)
    expected_log_ka_at_time_zero = compute_fermi_log_ka(0.0, T, tf)
    log_ka_diff = abs(expected_log_ka_at_time_zero - log_ka_at_time_zero)
    error_msg = "Expected %.2e, got %.2e" % (expected_log_ka_at_time_zero,
                                             log_ka_at_time_zero)
    nose.tools.ok_(log_ka_diff < EPSILON, error_msg)
    print error_msg
