import datetime
import typing
from types import TracebackType

from currency_convert.domain.agency.entities.interface import UnprocessedRate


class XmlParser(typing.Protocol):
    def parse(self, xml: str) -> dict[str, typing.Any]: ...


class ResponseLike(typing.Protocol):
    @property
    def text(self) -> str: ...
    def raise_for_status(self) -> typing.Self: ...
    def json(self, **kwargs: typing.Any) -> typing.Any: ...


class RequestHandler(typing.Protocol):
    def __enter__(self) -> typing.Self: ...

    def __exit__(
        self,
        exc_type: typing.Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None: ...

    def get(self, url: str, **kwargs: typing.Any) -> ResponseLike: ...


class EZBUpdateStrategy:
    URL: typing.ClassVar[str] = "https://data-api.ecb.europa.eu/service"
    RECOURCE: typing.ClassVar[str] = "data"
    TYPE: typing.ClassVar[str] = "EXR"
    KEY: typing.ClassVar[str] = "D..EUR.SP00.A"
    ERR_MESSAGE: typing.ClassVar[str] = "Unexpected data structure: %s"

    def __init__(
        self,
        request_handler: RequestHandler,
        xml_parser: XmlParser,
        from_date: datetime.datetime | None = None,
    ) -> None:
        self._request_handler = request_handler
        self._xml_parser = xml_parser
        self._from_date = from_date or (
            datetime.datetime.now(tz=datetime.timezone.utc) - datetime.timedelta(days=1)
        )

    def __call__(self) -> list[UnprocessedRate]:
        url = f"{self.URL}/{self.RECOURCE}/{self.TYPE}/{self.KEY}"
        params = {"updatedAfter": self._from_date.isoformat()}

        with self._request_handler as request_handler:
            response = request_handler.get(url, params=params).raise_for_status()
            data = self._xml_parser.parse(response.text)
            return self._match_data(data)

    def _match_data(self, data: dict[str, typing.Any]) -> list[UnprocessedRate]:
        match data:
            case {
                "message:GenericData": {
                    "message:DataSet": {"generic:Series": list() as series}
                }
            }:
                return self._iter_series(series)
            case _:
                raise ValueError(self.ERR_MESSAGE % data)

    def _iter_series(
        self, series: list[dict[str, typing.Any]]
    ) -> list[UnprocessedRate]:
        return [self._parse(s) for s in series]

    def _parse(self, series: dict[str, typing.Any]) -> UnprocessedRate:
        match series:
            case {
                "generic:SeriesKey": {
                    "generic:Value": [
                        _,
                        {
                            "@id": "CURRENCY",
                            "@value": currency_from,
                        },
                        {
                            "@id": "CURRENCY_DENOM",
                            "@value": currency_to,
                        },
                        *_,
                    ]
                },
                "generic:Obs": {
                    "generic:ObsDimension": {"@value": date},
                    "generic:ObsValue": {"@value": rate},
                },
            }:
                return UnprocessedRate(
                    currency_from=currency_from,
                    currency_to=currency_to,
                    rate=rate,
                    date=date,
                )
            case _:
                raise ValueError(self.ERR_MESSAGE % series)
