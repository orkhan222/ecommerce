from django.shortcuts import get_object_or_404

class ObjectRelationMixin:
    model = None
    relation = None
    slug = None
    def relations_in_object(self, relation=relation):
        obj = get_object_or_404(cat_slug=self.slug)
        relation = [r for r in obj.relation.all()]
        return relation
