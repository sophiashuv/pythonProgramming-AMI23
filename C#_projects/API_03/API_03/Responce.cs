using System;
using System.Collections.Generic;

namespace API_03
{
    
    public class Responce<T>
    {
        public Responce() { }

        public Responce(List<T> data, int count)
        {
            Data = data;
            Count = count;
        }
        
        public List<T> Data { get; set; }
           
        public int Count { get; set; }
    }
}