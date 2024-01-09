set(srcs
    "src/io/ioutils.c"
    "src/io/sink_wavwrite.c"
    "src/io/sink.c"
    "src/io/source_wavread.c"
    "src/io/source.c"
    "src/onset/peakpicker.c"
    "src/spectral/fft.c"
    "src/spectral/ooura_fft8g.c"
    "src/spectral/phasevoc.c"
    "src/spectral/specdesc.c"
    "src/spectral/statistics.c"
    "src/tempo/beattracking.c"
    "src/tempo/tempo.c"
    "src/temporal/biquad.c"
    "src/temporal/filter.c"
    "src/utils/hist.c"
    "src/utils/log.c"
    "src/utils/scale.c"
    "src/cvec.c"
    "src/fmat.c"
    "src/fvec.c"
    "src/lvec.c"
    "src/mathutils.c"
    "src/musicutils.c"
    "src/vecutils.c"
)

set(incs "src")

set(priv_incs
)

set(priv_reqs
)

idf_component_register(
    SRCS ${srcs}
    PRIV_INCLUDE_DIRS ${priv_incs}
    INCLUDE_DIRS ${incs}
    PRIV_REQUIRES ${priv_reqs}
    REQUIRES ${reqs}
)

# https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-guides/build-system.html#controlling-component-compilation
# When using these commands, place them after the call to idf_component_register in the component CMakeLists file.

component_compile_definitions(
    #HAVE_CONFIG_H
    HAVE_STDLIB_H
    HAVE_STDIO_H
    HAVE_COMPLEX_H
    #HAVE_FFTW3
    #HAVE_FFTW3F
    HAVE_MATH_H
    HAVE_STRING_H
    HAVE_ERRNO_H
    HAVE_LIMITS_H
    HAVE_STDARG_H
    #HAVE_BLAS
    HAVE_WAVWRITE
    AUBIO_BEAT_WARNINGS=1
)