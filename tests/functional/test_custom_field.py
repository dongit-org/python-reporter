from reporter import Reporter
from .utils import Artisan


def test_custom_field_operations(rc: Reporter, artisan: Artisan) -> None:
    # Create a custom field through Artisan, as there is currently no way to do so through the API
    output = artisan.execute(
        """
        $field = \\App\\Models\\CustomField::factory()->create([
            'name' => 'test_custom_field',
            'description' => 'Test custom field',
        ]);
        echo $field->id;
    """
    )
    custom_field_id = output.strip()

    custom_fields = rc.custom_fields.list()

    assert len(custom_fields) > 0
    assert custom_fields[0].id == custom_field_id
    assert custom_fields[0].name == "c_test_custom_field"
    assert custom_fields[0].description == "Test custom field"
