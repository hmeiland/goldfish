from django.urls import reverse, reverse_lazy
from django.views.generic import ListView,CreateView,UpdateView,DeleteView
from .models import VizNode,VizNodeList



class ListListView(ListView):
    model = VizNodeList
    template_name = "viz/index.html"

class ItemListView(ListView):
    model = VizNode
    template_name = "viz/viznode_list.html"
    
    def get_queryset(self):
        return VizNode.objects.filter(viznode_list_id=self.kwargs["list_id"])
    
    def get_context_data(self):
        context = super().get_context_data()
        context["viznode_list"] = VizNodeList.objects.get(id=self.kwargs["list_id"])
        return context
    
class ListCreate(CreateView):
    model = VizNodeList
    fields = ["title"]

    def get_context_data(self):
        context = super(ListCreate, self).get_context_data()
        context["title"] = "Add a new list"
        return context
    
class ItemCreate(CreateView):
    model = VizNode
    fields = [
        "viznode_list",
        "title",
        "description",
        "due_date",
    ]

    def get_initial(self):
        initial_data = super(ItemCreate, self).get_initial()
        viznode_list = VizNodeList.objects.get(id=self.kwargs["list_id"])
        initial_data["viznode_list"] = viznode_list
        return initial_data

    def get_context_data(self):
        context = super(ItemCreate, self).get_context_data()
        viznode_list = VizNodeList.objects.get(id=self.kwargs["list_id"])
        context["viznode_list"] = viznode_list
        context["title"] = "Create a new item"
        return context

    def get_success_url(self):
        VizNode.send_message()
        return reverse("list", args=[self.object.viznode_list_id])
    
class ItemUpdate(UpdateView):
    model = VizNode
    fields = [
        "viznode_list",
        "title",
        "description",
        "due_date",
    ]

    def get_context_data(self):
        context = super(ItemUpdate, self).get_context_data()
        context["viznode_list"] = self.object.viznode_list
        context["title"] = "Edit item"
        return context

    def get_success_url(self):
        return reverse("list", args=[self.object.viznode_list_id])

class ListDelete(DeleteView):
    model = VizNodeList
    # You have to use reverse_lazy() instead of reverse(),
    # as the urls are not loaded when the file is imported.
    success_url = reverse_lazy("index")

class ItemDelete(DeleteView):
    model = VizNode

    def get_success_url(self):
        return reverse_lazy("list", args=[self.kwargs["list_id"]])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["viznode_list"] = self.object.viznode_list
        return context