import generate_field
import visualize
battlefield = visualize.read_field('field.txt')
print(visualize.field_to_str(battlefield))
my = generate_field.generate_field()
print(visualize.field_to_str(my))