from django.views import generic

from offers.models import Category, Country, Offer


class IndexView(generic.ListView):
    context_object_name = "featured_offer_list"
    template_name = "offers/index.html"

    def get_queryset(self):
        return Offer.objects.raw(
            """
            SELECT *
            FROM (
                SELECT *,
                    ROW_NUMBER() OVER (PARTITION BY country_id ORDER BY id) AS rn
                FROM offers_offer
                WHERE featured = TRUE
            ) AS subquery
            WHERE rn = 1
            """
        )

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context["country_list"] = Country.objects.all()
        context["category_list"] = Category.objects.all()
        return context


class OfferListView(generic.ListView):
    model = Offer
    context_object_name = "offer_list"

    def get_queryset(self):
        offers = Offer.objects.all()
        offer = self.request.GET.get("offer")
        if offer is not None:
            offers = offers.filter(name__icontains=offer)
        country = self.request.GET.get("country")
        if country is not None:
            offers = offers.filter(country__id__exact=country)
        categories = self.request.GET.getlist("categories")
        if categories:
            offers = offers.filter(categories__id__in=categories).distinct()
        return offers

    def get_context_data(self, **kwargs):
        context = super(OfferListView, self).get_context_data(**kwargs)
        context["country_name_list"] = Country.objects.values_list("name", flat=True)
        context["category_name_list"] = Category.objects.values_list("name", flat=True)
        return context


class OfferDetailView(generic.DetailView):
    model = Offer


class CountryListView(generic.ListView):
    model = Country
    context_object_name = "country_list"
    queryset = Country.objects.all()


class CountryDetailView(generic.DetailView):
    model = Country


class CategoryListView(generic.ListView):
    model = Category
    context_object_name = "category_list"
    queryset = Category.objects.all()


class CategoryDetailView(generic.DetailView):
    model = Category
