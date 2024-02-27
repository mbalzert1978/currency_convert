from currency_convert.core.domain.shared.error import Error


class AgencyAllreadExistsError(Error):

    """Error when trying to create an agency that already exists."""
