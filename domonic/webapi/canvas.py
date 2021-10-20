"""
    domonic.webapi.canvas
    ====================================
    https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API
"""


# class Canvas:
#     """
#     The Canvas API provides methods for drawing on a canvas.
#     """

#     def __init__(self, canvas):
#         self.canvas = canvas

#     def getContext(self, context_type):
#         """
#         Returns a drawing context on this canvas, or null if the context
#         identifier is not supported.
#         """
#         return self.canvas.getContext(context_type)

#     def toDataURL(self, type, encoder_options):
#         """
#         Returns a data URL containing a representation of the image in the
#         format specified by type (defaults to PNG).
#         """
#         return self.canvas.toDataURL(type, encoder_options)

#     def toBlob(self, type, encoder_options):
#         """
#         Returns a Blob object representing the image in the format specified by
#         type (defaults to PNG).
#         """
#         return self.canvas.toBlob(type, encoder_options)

#     def toBuffer(self, type, encoder_options):
#         """
#         Returns a Buffer object representing the image in the format specified
#         by type (defaults to PNG).
#         """
#         return self.canvas.toBuffer(type, encoder_options)