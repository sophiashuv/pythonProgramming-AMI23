using System;
using System.ComponentModel;
namespace Classes_1
{
    public class Product
    /* Class for Product representation. */
    {
        private string id,title, created_at, updated_at, image_url, description;
        private double price;

        public Product InputProduct()
        {
            foreach (PropertyDescriptor prop in TypeDescriptor.GetProperties(this))
            {
                if (prop.Name != "Id")
                {
                    Console.Write($"{prop.Name}: ");
                    prop.SetValue(this, Convert.ChangeType(Console.ReadLine(), prop.PropertyType));
                }
                this.Id = Guid.NewGuid().ToString();
            }
            return this;
        }
        
        public string Id { get; set; }
        public string Description { get; set; }
        
        public string Title
        {
            get => title; 
            set => title = Validation.ValidateTitle(value); 
        }
        
        public string Image_url
        {
            get => image_url; 
            set => image_url = Validation.ValidateImage_url(value); 
        }
        
        public double Price
        {
            get => price;
            set => price = Validation.ValidatePrice(value); 
        }
        
        public string Created_at
        {
            get => created_at;
            set => created_at = Validation.ValidateDate(value); 
        }
        
        public string Updated_at
        {
            get => updated_at; 
            set => updated_at = Validation.ValidateDate(created_at, value); 
        }

        public override string ToString() {
            string res = "";
            foreach (PropertyDescriptor prop in TypeDescriptor.GetProperties(this)) 
                res += ($"{prop.Name}: {prop.GetValue(this)}\n");
            return res.Substring(0, res.Length-1);
        }
    }
}