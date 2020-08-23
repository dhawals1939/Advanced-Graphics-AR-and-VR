def corrdinate_to_wrc(x, directional_extreme):
    center_factor = -int((directional_extreme + 2) / 2 - 1)
    return x + center_factor
