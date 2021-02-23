using System;
using System.ComponentModel;
using System.ComponentModel.DataAnnotations;

namespace task02_Generics
{
    public class Product: BaseClass
        /* Class for Product representation. */
    {
        private string title, created_at, updated_at, image_url;
        private double price;

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
    }
}