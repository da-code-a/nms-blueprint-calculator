export async function getBlueprintsByCategory(category) {
    if (!category) {
        category = ''
    };
    const response = await fetch(`/api/blueprints/${category}`);
    return await response.json();
}
