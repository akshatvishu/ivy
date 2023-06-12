import jax.numpy as jnp
from typing import Optional
from ivy.functional.backends.jax import JaxArray
from ivy.func_wrapper import with_supported_device_and_dtypes
from . import backend_version


@with_supported_device_and_dtypes(
    {
        "0.4.10 and below": {
            "cpu": (
                "float16",
                "float32",
                "float64",
            )
        }
    },
    backend_version,
)
def l1_normalize(
    x: JaxArray,
    /,
    *,
    axis: Optional[int] = None,
    out: Optional[JaxArray] = None,
) -> JaxArray:
    denorm = jnp.linalg.norm(x, 1, axis, keepdims=True)
    return jnp.divide(x, denorm)


def l2_normalize(
    x: JaxArray,
    /,
    *,
    axis: Optional[int] = None,
    out: Optional[JaxArray] = None,
) -> JaxArray:
    if axis is None:
        denorm = jnp.linalg.norm(x.flatten(), 2, axis)
    else:
        denorm = jnp.linalg.norm(x, 2, axis, keepdims=True)
    denorm = jnp.maximum(denorm, 1e-12)
    return x / denorm


def lp_normalize(
    x: JaxArray,
    /,
    *,
    p: float = 2,
    axis: Optional[int] = None,
    out: Optional[JaxArray] = None,
) -> JaxArray:
    if axis is None:
        denorm = jnp.linalg.norm(x.flatten(), axis=axis, ord=p)
    else:
        denorm = jnp.linalg.norm(x, axis=axis, ord=p, keepdims=True)

    denorm = jnp.maximum(denorm, 1e-12)
    return jnp.divide(x, denorm)
