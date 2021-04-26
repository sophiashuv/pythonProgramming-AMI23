using System.Collections.Generic;
using System.Threading.Tasks;
using Sophia.Models;

namespace Sophia.Cache
{
    public interface IRedisCache
    {
        List<Product> GetProducts(string searchString, string sortOrder,
            string sortType, int offset, int limit);
        void SetProducts(string searchString, string sortOrder,
            string sortType, int offset, int limit, List<Product>  products);
        void RemoveAllCache();
    }
}