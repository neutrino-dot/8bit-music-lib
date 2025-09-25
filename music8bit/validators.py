def check_Val_Typ(value, expected_type, least_range=None, most_range=None, name="value"):
    # 型チェック
    if not isinstance(value, expected_type):
        # expected_type がタプルなら型名をまとめる
        if isinstance(expected_type, tuple):
            type_names = ", ".join(t.__name__ for t in expected_type)
        else:
            type_names = expected_type.__name__
        raise TypeError(f"{name} must be {type_names}, got {type(value).__name__}")

    # 数値型なら範囲チェック（int, float など）
    if isinstance(value, numbers.Real):
        if least_range is not None and value < least_range:
            raise ValueError(f"{name} must be >= {least_range}, got {value}")
        if most_range is not None and value > most_range:
            raise ValueError(f"{name} must be <= {most_range}, got {value}")

    return value