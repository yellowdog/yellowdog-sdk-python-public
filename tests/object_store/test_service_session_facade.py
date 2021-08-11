from yellowdog_client.object_store import ServiceSessionFacade


class TestEnqueueChunkUpload(object):
    def test(self, mocker):
        task = mocker.MagicMock()
        engine = mocker.MagicMock()

        facade = ServiceSessionFacade()
        facade.upload_engine = engine

        facade.enqueue_chunk_upload(chunk_upload_task=task)

        engine.enqueue_chunk_transfer_task.assert_called_once_with(chunk_task=task)


class TestEnqueueChunkDownload(object):
    def test(self, mocker):
        task = mocker.MagicMock()
        engine = mocker.MagicMock()

        facade = ServiceSessionFacade()
        facade.download_engine = engine

        facade.enqueue_chunk_download(chunk_download_task=task)

        engine.enqueue_chunk_transfer_task.assert_called_once_with(chunk_task=task)


class TestAbort(object):
    def test(self, mocker):
        proxy = mocker.MagicMock()

        facade = ServiceSessionFacade()
        facade.object_store_service_proxy = proxy
        facade.session_id = "my_session_id"

        facade.abort()

        proxy.abort_transfer.assert_called_once_with(session_id="my_session_id")


class TestComplete(object):
    def test(self, mocker):
        proxy = mocker.MagicMock()

        facade = ServiceSessionFacade()
        facade.object_store_service_proxy = proxy
        facade.session_id = "my_session_id"

        facade.complete(summary_hash="my_summary_hash")

        proxy.complete_transfer.assert_called_once_with(session_id="my_session_id", summary_hash="my_summary_hash")


class TestServerChunksTransferred(object):
    def test(self, mocker):
        proxy_response = mocker.MagicMock()
        proxy_response.chunksReceived = 700

        proxy = mocker.MagicMock()
        proxy.get_transfer_status.return_value = proxy_response

        facade = ServiceSessionFacade()
        facade.object_store_service_proxy = proxy
        facade.session_id = "my_session_id"

        res = facade.server_chunks_transferred

        proxy.get_transfer_status.assert_called_once_with(session_id="my_session_id")

        assert res == 700


class TestCreateThread(object):
    def test(self, mocker):
        factory = mocker.MagicMock()
        factory.new_thread.return_value = "my_new_thread"

        facade = ServiceSessionFacade()
        facade.thread_factory = factory

        res = facade.create_thread(target=TestCreateThread.test)

        factory.new_thread.assert_called_once_with(target=TestCreateThread.test)
        assert res == "my_new_thread"


class TestDispatchNotification(object):
    def test(self, mocker):
        handler = mocker.MagicMock()
        args = mocker.MagicMock()

        dispatcher = mocker.MagicMock()

        facade = ServiceSessionFacade()
        facade.notification_dispatcher = dispatcher

        facade.dispatch_notification(event_handler=handler, event_args=args)

        dispatcher.dispatch.assert_called_once_with(event_handler=handler, event_args=args)
