from django.db import models
from django.contrib.auth.models import User

class Blog(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
 

from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    image = models.ImageField(upload_to='products/', null=True, blank=True)

    def __str__(self):
        return self.name


from django.contrib.auth.models import User
from django.db import models

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()



# analyze

class FarmAnalysis(models.Model):
    date = models.DateField()  # Date when the analysis was performed
    income = models.IntegerField()  # Income from the farm
    expenses = models.IntegerField()  # Expenses for the farm
    harvested_quantity = models.IntegerField()  # Harvested quantity of produce
    profit_loss = models.IntegerField()  # Profit or loss (calculated field, income - expenses)
    
    def save(self, *args, **kwargs):
        # Calculate profit or loss when saving the record
        self.profit_loss = self.income - self.expenses
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Farm Analysis on {self.date}"