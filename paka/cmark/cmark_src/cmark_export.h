
#ifndef CMARK_EXPORT_H
#define CMARK_EXPORT_H

#ifdef CMARK_STATIC_DEFINE
#  define CMARK_EXPORT
#  define CMARK_NO_EXPORT
#else
#  ifndef CMARK_EXPORT
#    ifdef cmark_EXPORTS
        /* We are building this library */
#      ifdef _MSC_VER
#        define CMARK_EXPORT __declspec(dllexport)
#      else
#        define CMARK_EXPORT __attribute__((visibility("default")))
#      endif
#    else
        /* We are using this library */
#      ifdef _MSC_VER
#        define CMARK_EXPORT __declspec(dllimport)
#      else
#        define CMARK_EXPORT __attribute__((visibility("default")))
#      endif
#    endif
#  endif

#  ifndef CMARK_NO_EXPORT
#    ifdef _MSC_VER
#      define CMARK_NO_EXPORT
#    else
#      define CMARK_NO_EXPORT __attribute__((visibility("hidden")))
#    endif
#  endif
#endif

#ifndef CMARK_DEPRECATED
#  ifdef _MSC_VER
#    define CMARK_DEPRECATED __declspec(deprecated)
#  else
#    define CMARK_DEPRECATED __attribute__((__deprecated__))
#  endif
#endif

#ifndef CMARK_DEPRECATED_EXPORT
#  define CMARK_DEPRECATED_EXPORT CMARK_EXPORT CMARK_DEPRECATED
#endif

#ifndef CMARK_DEPRECATED_NO_EXPORT
#  define CMARK_DEPRECATED_NO_EXPORT CMARK_NO_EXPORT CMARK_DEPRECATED
#endif

#if 0 /* DEFINE_NO_DEPRECATED */
#  ifndef CMARK_NO_DEPRECATED
#    define CMARK_NO_DEPRECATED
#  endif
#endif

#endif
