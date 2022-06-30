import stt

class model():
    def __init__(self, model_path):
        self._impl = None

        status, impl = stt.impl.CreateModel(model_path)

        if status != 0:
            raise RuntimeError("CreateModel failed with '{}' (0x{:X})".format(
                    stt.impl.ErrorCodeToErrorMessage(status), status
                )
            )

        self._impl = impl

    def __del__(self):
        if self._impl:
            stt.impl.FreeModel(self._impl)
            self._impl = None

    def beamWidth(self):

        return stt.impl.GetModelBeamWidth(self._impl)

    def sampleRate(self):
        return stt.impl.GetModelSampleRate(self._impl)

    def enableExternalScorer(self, scorer_path):
        status = stt.impl.EnableExternalScorer(self._impl, scorer_path)
        if status != 0:
            raise RuntimeError(
                "EnableExternalScorer failed with '{}' (0x{:X})".format(
                    stt.impl.ErrorCodeToErrorMessage(status), status
                )
            )

    def disableExternalScorer(self):
        return stt.impl.DisableExternalScorer(self._impl)

    def addHotWord(self, word, boost):
        status = stt.impl.AddHotWord(self._impl, word, boost)
        if status != 0:
            raise RuntimeError(
                "AddHotWord failed with '{}' (0x{:X})".format(
                    stt.impl.ErrorCodeToErrorMessage(status), status
                )
            )

    def eraseHotWord(self, word):
        status = stt.impl.EraseHotWord(self._impl, word)
        if status != 0:
            raise RuntimeError(
                "EraseHotWord failed with '{}' (0x{:X})".format(
                    stt.impl.ErrorCodeToErrorMessage(status), status
                )
            )
        


    def setScorerAlphaBeta(self, alpha, beta):
        """
        Set hyperparameters alpha and beta of the external scorer.

        :param alpha: The alpha hyperparameter of the decoder. Language model weight.
        :type alpha: float

        :param beta: The beta hyperparameter of the decoder. Word insertion weight.
        :type beta: float

        :return: Zero on success, non-zero on failure.
        :type: int
        """
        return stt.impl.SetScorerAlphaBeta(self._impl, alpha, beta)


    def stt(self, audio_buffer):
        """
        Use the Coqui STT model to perform Speech-To-Text.

        :param audio_buffer: A 16-bit, mono audio signal at the appropriate sample rate (matching what the model was trained on).
        :type audio_buffer: numpy.int16 array

        :return: The STT result.
        :type: str
        """
        return stt.impl.SpeechToText(self._impl, audio_buffer)



    def sttWithMetadata(self, audio_buffer, num_results=1):
        """
        Use the Coqui STT model to perform Speech-To-Text and return results including metadata.

        :param audio_buffer: A 16-bit, mono raw audio signal at the appropriate sample rate (matching what the model was trained on).
        :type audio_buffer: numpy.int16 array

        :param num_results: Maximum number of candidate transcripts to return. Returned list might be smaller than this.
        :type num_results: int

        :return: Metadata object containing multiple candidate transcripts. Each transcript has per-token metadata including timing information.
        :type: :func:`Metadata`
        """
        return stt.impl.SpeechToTextWithMetadata(self._impl, audio_buffer, num_results)

    def createStream(self):
        """
        Create a new streaming inference state. The streaming state returned by
        this function can then be passed to :func:`feedAudioContent()` and :func:`finishStream()`.

        :return: Stream object representing the newly created stream
        :type: :func:`Stream`

        :throws: RuntimeError on error
        """
        status, ctx = stt.impl.CreateStream(self._impl)
        if status != 0:
            raise RuntimeError(
                "CreateStream failed with '{}' (0x{:X})".format(
                    stt.impl.ErrorCodeToErrorMessage(status), status
                )
            )
        return Stream(ctx)


class Stream(object):
    """
    Class wrapping a stt stream. The constructor cannot be called directly.
    Use :func:`Model.createStream()`
    """

    def __init__(self, native_stream):
        self._impl = native_stream

    def __del__(self):
        if self._impl:
            self.freeStream()

    def feedAudioContent(self, audio_buffer):
        """
        Feed audio samples to an ongoing streaming inference.

        :param audio_buffer: A 16-bit, mono raw audio signal at the appropriate sample rate (matching what the model was trained on).
        :type audio_buffer: numpy.int16 array

        :throws: RuntimeError if the stream object is not valid
        """
        if not self._impl:
            raise RuntimeError(
                "Stream object is not valid. Trying to feed an already finished stream?"
            )
        stt.impl.FeedAudioContent(self._impl, audio_buffer)

    def intermediateDecode(self):
        """
        Compute the intermediate decoding of an ongoing streaming inference.

        :return: The STT intermediate result.
        :type: str

        :throws: RuntimeError if the stream object is not valid
        """
        if not self._impl:
            raise RuntimeError(
                "Stream object is not valid. Trying to decode an already finished stream?"
            )
        return stt.impl.IntermediateDecode(self._impl)

    def intermediateDecodeWithMetadata(self, num_results=1):
        """
        Compute the intermediate decoding of an ongoing streaming inference and return results including metadata.

        :param num_results: Maximum number of candidate transcripts to return. Returned list might be smaller than this.
        :type num_results: int

        :return: Metadata object containing multiple candidate transcripts. Each transcript has per-token metadata including timing information.
        :type: :func:`Metadata`

        :throws: RuntimeError if the stream object is not valid
        """
        if not self._impl:
            raise RuntimeError(
                "Stream object is not valid. Trying to decode an already finished stream?"
            )
        return stt.impl.IntermediateDecodeWithMetadata(self._impl, num_results)

    def intermediateDecodeFlushBuffers(self):
        """
        EXPERIMENTAL: Compute the intermediate decoding of an ongoing streaming
        inference, flushing buffers first. This ensures that all audio that has
        been streamed so far is included in the result, but is more expensive
        than intermediateDecode() because buffers are processed through the
        acoustic model.

        :return: The STT intermediate result.
        :type: str

        :throws: RuntimeError if the stream object is not valid
        """
        if not self._impl:
            raise RuntimeError(
                "Stream object is not valid. Trying to decode an already finished stream?"
            )
        return stt.impl.intermediateDecodeFlushBuffers(self._impl)

    def intermediateDecodeWithMetadataFlushBuffers(self, num_results=1):
        """
        EXPERIMENTAL: Compute the intermediate decoding of an ongoing streaming
        inference, flushing buffers first. This ensures that all audio that has
        been streamed so far is included in the result, but is more expensive
        than intermediateDecode() because buffers are processed through the
        acoustic model. Returns results including metadata.

        :param num_results: Maximum number of candidate transcripts to return. Returned list might be smaller than this.
        :type num_results: int

        :return: Metadata object containing multiple candidate transcripts. Each transcript has per-token metadata including timing information.
        :type: :func:`Metadata`

        :throws: RuntimeError if the stream object is not valid
        """
        if not self._impl:
            raise RuntimeError(
                "Stream object is not valid. Trying to decode an already finished stream?"
            )
        return stt.impl.intermediateDecodeWithMetadataFlushBuffers(
            self._impl, num_results
        )

    def finishStream(self):
        """
        Compute the final decoding of an ongoing streaming inference and return
        the result. Signals the end of an ongoing streaming inference. The underlying
        stream object must not be used after this method is called.

        :return: The STT result.
        :type: str

        :throws: RuntimeError if the stream object is not valid
        """
        if not self._impl:
            raise RuntimeError(
                "Stream object is not valid. Trying to finish an already finished stream?"
            )
        result = stt.impl.FinishStream(self._impl)
        self._impl = None
        return result

    def finishStreamWithMetadata(self, num_results=1):
        """
        Compute the final decoding of an ongoing streaming inference and return
        results including metadata. Signals the end of an ongoing streaming
        inference. The underlying stream object must not be used after this
        method is called.

        :param num_results: Maximum number of candidate transcripts to return. Returned list might be smaller than this.
        :type num_results: int

        :return: Metadata object containing multiple candidate transcripts. Each transcript has per-token metadata including timing information.
        :type: :func:`Metadata`

        :throws: RuntimeError if the stream object is not valid
        """
        if not self._impl:
            raise RuntimeError(
                "Stream object is not valid. Trying to finish an already finished stream?"
            )
        result = stt.impl.FinishStreamWithMetadata(self._impl, num_results)
        self._impl = None
        return result


    def freeStream(self):
        """
        Destroy a streaming state without decoding the computed logits. This can
        be used if you no longer need the result of an ongoing streaming inference.

        :throws: RuntimeError if the stream object is not valid
        """
        if not self._impl:
            raise RuntimeError(
                "Stream object is not valid. Trying to free an already finished stream?"
            )
        stt.impl.FreeStream(self._impl)
        self._impl = None
