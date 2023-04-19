import numpy as np

class RfPart:
    def __init__(self, frequency   =None,
                       gain        =None,
                       noise_figure=None,
                       input_p1db  =None,
                       input_ip2   =None,
                       input_ip3   =None,
                       input_pmax  =None):
        self.frequency    = np.array(frequency)    if frequency    is not None else np.zeros(0)
        self.gain         = np.array(gain)         if gain         is not None else np.zeros(0)
        self.noise_figure = np.array(noise_figure) if noise_figure is not None else np.zeros(0)
        self.input_p1db   = np.array(input_p1db)   if input_p1db   is not None else np.zeros(0)
        self.input_ip2    = np.array(input_ip2)    if input_ip2    is not None else np.zeros(0)
        self.input_ip3    = np.array(input_ip3)    if input_ip3    is not None else np.zeros(0)
        self.input_pmax   = np.array(input_pmax)   if input_pmax   is not None else np.zeros(0)

    @staticmethod
    def db_to_linear(value):
        return 10**(value / 10)

    @staticmethod
    def linear_to_db(value):
        return 10 * np.log10(value)

    @staticmethod
    def cascade_gain(gains):
        return np.sum(gains, axis=0)

    @staticmethod
    def cascade_noise_figure(gains, noise_figures):
        gains_linear = np.array([RfPart.db_to_linear(g)  for g  in gains])
        nf_linear    = np.array([RfPart.db_to_linear(nf) for nf in noise_figures])
        nf_cascade_linear = nf_linear[0] + np.sum([(nf_linear[i] - 1) / np.prod(gains_linear[:i], axis=0) for i in range(1, len(nf_linear))], axis=0)
        return RfPart.linear_to_db(nf_cascade_linear)

    @staticmethod
    def cascade_input_p(gains, p_values):
        adjusted_p_values = np.array([p_values[i] - np.sum(gains[:i], axis=0) for i in range(len(p_values))])
        return np.min(adjusted_p_values, axis=0)

    @staticmethod
    def cascade(rfpart_list):
        if not rfpart_list:
            return RfPart()
        
        frequencies   = rfpart_list[0].frequency
        gains =         [part.gain         for part in rfpart_list]
        noise_figures = [part.noise_figure for part in rfpart_list]
        input_p1dbs =   [part.input_p1db   for part in rfpart_list]
        input_ip2s =    [part.input_ip2    for part in rfpart_list]
        input_ip3s =    [part.input_ip3    for part in rfpart_list]
        input_pmaxs =   [part.input_pmax   for part in rfpart_list]

        cascaded_gain         = RfPart.cascade_gain(np.vstack(gains))
        cascaded_noise_figure = RfPart.cascade_noise_figure(np.vstack(gains), np.vstack(noise_figures))
        cascaded_input_p1db   = RfPart.cascade_input_p(     np.vstack(gains), np.vstack(input_p1dbs))
        cascaded_input_ip2    = RfPart.cascade_input_p(     np.vstack(gains), np.vstack(input_ip2s))
        cascaded_input_ip3    = RfPart.cascade_input_p(     np.vstack(gains), np.vstack(input_ip3s))
        cascaded_input_pmax   = RfPart.cascade_input_p(     np.vstack(gains), np.vstack(input_pmaxs))

        return RfPart(frequencies,
                      cascaded_gain,
                      cascaded_noise_figure,
                      cascaded_input_p1db,
                      cascaded_input_ip2,
                      cascaded_input_ip3,
                      cascaded_input_pmax)

    def find_common_factor(self, arr):
        factors = [ 1e9,   1e6,   1e3,   1]
        labels  = ['1e9', '1e6', '1e3', '1']
        for i, factor in enumerate(factors):
            min_val = min(arr / factor)
            if min_val >= 1:
                return factor, labels[i]
        return 1, '1'

    def __repr__(self):
        def format_array(arr):
            if len(arr) > 5:
                formatted = " ".join([f"{a:7.3f}" for a in arr[:3]]) + " ... " + " ".join([f"{a:7.3f}" for a in arr[-2:]])
            else:
                formatted = " ".join([f"{a:7.3f}" for a in arr])
            return formatted

        freq_factor, factor_label = self.find_common_factor(self.frequency)
        freq_str = format_array(self.frequency / freq_factor)
        gain_str = format_array(self.gain)
        nf_str   = format_array(self.noise_figure)
        p1db_str = format_array(self.input_p1db)
        ip2_str  = format_array(self.input_ip2)
        ip3_str  = format_array(self.input_ip3)
        pmax_str = format_array(self.input_pmax)

        factor_str = f"*{factor_label}" if freq_factor != 1 else ""

        return (f"RfPart(frequency   =[ {freq_str}]{factor_str} ({len(self.frequency)} points),\n"
                f"       gain        =[ {gain_str}],\n"
                f"       noise_figure=[ {nf_str}],\n"
                f"       input_p1db  =[ {p1db_str}],\n"
                f"       input_ip2   =[ {ip2_str}],\n"
                f"       input_ip3   =[ {ip3_str}],\n"
                f"       input_pmax  =[ {pmax_str}]\n"
                f")")
