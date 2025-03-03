from typing import List, Optional, Dict, Any
from app.models.category import Category
from app.exceptions.customer_exceptions import NotFoundException, BadRequestException
from peewee import DoesNotExist, IntegrityError


class CategoryService:
    @staticmethod
    def get_all_categories() -> List[Dict[str, Any]]:
        """Get all categories"""
        categories = Category.select()
        return [category.to_json() for category in categories]

    @staticmethod
    def get_category_tree() -> List[Dict[str, Any]]:
        """Get categories in a tree structure"""
        # Get all categories
        categories = Category.select().order_by(Category.id)
        
        # Create a dictionary of categories for quick lookup
        category_dict = {category.id: category.to_json() for category in categories}
        
        # Build the tree
        tree = []
        for category_id, category in category_dict.items():
            parent_id = category.get('parent_id')
            if parent_id is None:
                # This is a root category
                tree.append(category)
            else:
                # This is a child category
                if parent_id in category_dict:
                    if 'children' not in category_dict[parent_id]:
                        category_dict[parent_id]['children'] = []
                    category_dict[parent_id]['children'].append(category)
                else:
                    # Parent not found, treat as root
                    tree.append(category)
        
        return tree

    @staticmethod
    def get_category_by_id(category_id: int) -> Dict[str, Any]:
        """Get a category by ID"""
        try:
            category = Category.get_by_id(category_id)
            return category.to_json()
        except DoesNotExist:
            raise NotFoundException(f"Category with ID {category_id} not found")

    @staticmethod
    def get_children(category_id: int) -> List[Dict[str, Any]]:
        """Get all direct children of a category"""
        try:
            # Check if the parent category exists
            Category.get_by_id(category_id)
            
            children = Category.select().where(Category.parent_id == category_id)
            return [child.to_json() for child in children]
        except DoesNotExist:
            raise NotFoundException(f"Parent category with ID {category_id} not found")

    @staticmethod
    def get_descendants(category_id: int) -> List[Dict[str, Any]]:
        """Get all descendants of a category (children, grandchildren, etc.)"""
        try:
            # Check if the category exists
            Category.get_by_id(category_id)
            
            # Get direct children first
            children = CategoryService.get_children(category_id)
            descendants = children.copy()
            
            # Recursively get descendants
            for child in children:
                child_descendants = CategoryService.get_descendants(child['id'])
                descendants.extend(child_descendants)
                
            return descendants
        except DoesNotExist:
            raise NotFoundException(f"Category with ID {category_id} not found")

    @staticmethod
    def create_category(display_name: str, parent_id: Optional[int] = None) -> Dict[str, Any]:
        """Create a new category"""
        try:
            # If parent_id is provided, check if it exists
            if parent_id is not None:
                try:
                    Category.get_by_id(parent_id)
                except DoesNotExist:
                    raise NotFoundException(f"Parent category with ID {parent_id} not found")
            
            category = Category.create(display_name=display_name, parent_id=parent_id)
            return category.to_json()
        except IntegrityError as e:
            raise BadRequestException(f"Error creating category: {str(e)}")

    @staticmethod
    def update_category(category_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a category"""
        try:
            category = Category.get_by_id(category_id)
            
            # Update display_name if provided
            if 'display_name' in data:
                category.display_name = data['display_name']
            
            # Update parent_id if provided
            if 'parent_id' in data:
                parent_id = data['parent_id']
                
                # Prevent circular references
                if parent_id == category_id:
                    raise BadRequestException("A category cannot be its own parent")
                
                # Check if new parent exists
                if parent_id is not None:
                    try:
                        Category.get_by_id(parent_id)
                        
                        # Prevent creating loops in the hierarchy
                        descendants = CategoryService.get_descendants(category_id)
                        descendant_ids = [desc['id'] for desc in descendants]
                        if parent_id in descendant_ids:
                            raise BadRequestException("Cannot set a descendant as parent")
                    except DoesNotExist:
                        raise NotFoundException(f"Parent category with ID {parent_id} not found")
                
                category.parent_id = parent_id
            
            category.save()
            return category.to_json()
        except DoesNotExist:
            raise NotFoundException(f"Category with ID {category_id} not found")

    @staticmethod
    def delete_category(category_id: int, recursive: bool = False) -> Dict[str, str]:
        """Delete a category"""
        try:
            category = Category.get_by_id(category_id)
            
            # Check if the category has children
            children = Category.select().where(Category.parent_id == category_id)
            
            if children.exists() and not recursive:
                raise BadRequestException(
                    "Cannot delete category with children. Set recursive=True to delete all children as well."
                )
            
            if recursive:
                # Delete all descendants recursively
                descendants = CategoryService.get_descendants(category_id)
                for descendant in reversed(descendants):  # Delete from bottom up
                    Category.delete_by_id(descendant['id'])
            
            # Delete the category
            category.delete_instance()
            
            return {"message": f"Category {category_id} deleted successfully"}
        except DoesNotExist:
            raise NotFoundException(f"Category with ID {category_id} not found")
