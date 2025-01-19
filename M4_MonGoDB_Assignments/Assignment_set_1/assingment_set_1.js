//Find high spending users//
db.users.aggregate([
    {
        $lookup: {
            from: "orders",
            localField: "userId",
            foreignField: "userId",
            as: "userOrders"
        }
    },
    {
        $unwind: "$userOrders"
    },
    {
        $group: {
            _id: "$userId",
            totalSpent: { $sum: "$userOrders.totalAmount" }
        }
    },
    {
        $match: {
            totalSpent: { $gt: 500 }
        }
    },
    {
        $lookup: {
            from: "users",
            localField: "_id",
            foreignField: "userId",
            as: "userInfo"
        }
    },
    {
        $project: {
            userId: "$_id",
            totalSpent: 1,
            userInfo: { $arrayElemAt: ["$userInfo", 0] }
        }
    }
]);
//List Popular Products by Average rating//
db.products.aggregate([
    {
        $unwind: "$ratings"
    },
    {
        $group: {
            _id: "$productId",
            averageRating: { $avg: "$ratings.rating" }
        }
    },
    {
        $match: {
            averageRating: { $gte: 4 }
        }
    },
    {
        $lookup: {
            from: "products",
            localField: "_id",
            foreignField: "productId",
            as: "productInfo"
        }
    },
    {
        $project: {
            productId: "$_id",
            averageRating: 1,
            productInfo: { $arrayElemAt: ["$productInfo", 0] }
        }
    }
]);
//Search For orders in specific time range//
db.orders.aggregate([
    {
        $match: {
            orderDate: {
                $gte: ISODate("2024-12-01T00:00:00Z"),
                $lt: ISODate("2025-01-01T00:00:00Z")
            }
        }
    },
    {
        $lookup: {
            from: "users",
            localField: "userId",
            foreignField: "userId",
            as: "userInfo"
        }
    },
    {
        $unwind: "$userInfo"
    },
    {
        $project: {
            orderId: 1,
            orderDate: 1,
            totalAmount: 1,
            status: 1,
            userName: "$userInfo.name"
        }
    }
]);
//Update Stock After completion//
const order = {
    orderId: "ORD001",
    items: [
        { productId: "P001", quantity: 2 },
        { productId: "P002", quantity: 1 }
    ]
};

order.items.forEach(item => {
    db.products.updateOne(
        { productId: item.productId },
        { $inc: { stock: -item.quantity } }
    );
});
//Find the nearest warehouse//
// Assuming you have the coordinates of the user's location
const userLocation = {
    type: "Point",
    coordinates: [-74.006, 40.7128] // Example coordinates (longitude, latitude)
};

db.warehouses.aggregate([
    {
        $geoNear: {
            near: userLocation,
            distanceField: "distance",
            maxDistance: 50000, // 50 kilometers in meters
            spherical: true,
            query: {
                products: "P001" // Filter for warehouses that stock "P001"
            }
        }
    }
]);