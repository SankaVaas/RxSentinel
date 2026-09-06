import pytest
from unittest.mock import AsyncMock, patch

from app.tools.rxnorm_client import check_interaction


@pytest.mark.asyncio
async def test_check_interaction_returns_none_when_no_groups() -> None:
    with patch("app.tools.rxnorm_client.get_json", new=AsyncMock(return_value={"fullInteractionTypeGroup": []})):
        result = await check_interaction("111", "222")
    assert result is None


@pytest.mark.asyncio
async def test_check_interaction_maps_severity() -> None:
    mock_response = {
        "fullInteractionTypeGroup": [
            {
                "fullInteractionType": [
                    {
                        "interactionPair": [
                            {"severity": "major", "description": "Increased bleeding risk"}
                        ]
                    }
                ]
            }
        ]
    }
    with patch("app.tools.rxnorm_client.get_json", new=AsyncMock(return_value=mock_response)):
        result = await check_interaction("111", "222")
    assert result["severity"] == "high"
    assert "bleeding" in result["description"]
