# Angular Routing


## Introduction
Use the `routerLink` directive on buttons links etc. to have them navigate to the specified route on click. For example: `<a [routerLink]="['/products']">Product List</a>`

The angular router follows this chain: change in url -> match path -> process guards -> resolve data -> activate components -> display templates


## Routing Basics
To set up routing, we need to: define base path, import Router, configure routes, place templates, activate routes.


A base path is part of the URL that defines the path to the application subfolder on the server. For example, consider this url: `www.mysite.com/APM/`. Here, the base path is `/APM/`.

When deploying the application to production, we may want to change the base path. Use the angular cli to reset the base path before deploying to production: `ng build --base-href /APM/`

To use routing in an angular application, import the `RouterModule`. This module contains the Router service, several routing directives such as `routerLink` and other routing stuff.

The `RouterModule` can be imported multiple times in an angular application. Since the Router service deals with one globally shared resource - URLLocation - there can only be one active Router service. 

To ensure this, the router module provides two methods: `forRoot()` and `forChild()`

`forRoot()` is use once for the entire application. It declares the router directives, manages route configuration, and registers the router service.

`forChild()` declares the router directives, manages our route configuration, but does not register the router service. It is generally used in feature modules.

For each `router-outlet`, only one route path can be active at a time

A route configuration is an array of route objects. For example:
```
[
  {path: 'welcome', component: WelcomeComponent},
  {path: '', redirectTo: 'welcome', pathMatch: 'full'},
  {path: '**', component: PageNotFoundComponent}
]
```

A redirect route requires a `pathMatch` property.
A wildcard `'**'` path matches segments that did not match and of the other defined route paths.

Route paths are case sensitive.

Order of the routes in the array matters because the Router uses a first match wins strategy. More specific paths should be before less specific paths.

Redirects cannot be chained. After one redirect, the router stops.

`routerLink` is an attribute directive; we can add it to any clickable element. We bind the directive to a template expression that returns a link parameters array:
```
<a [routerLink]="['/welcome']">Home</a>
```

We can also use the shorthand syntax with a one time binding that points to a string:
```
<a routerLink="/welcome">Home</a>
```
This is because the route path is a string and doesn't change. See this SO question for the difference between property binding with and without square brackets: https://stackoverflow.com/questions/42977101/angular-2-difference-between-property-binding-with-and-without-brackets

We need to configure our web server if we're using HTML 5 style URLs to rewrite any in-app url segments to `index.html`. Then once the app loads, it processes the original URL.

To use hash based URLs, pass in `{ useHash: true }` in the `forRoot(...)` method.


## Routing to Features
Give each related feature route a similar route path name. For example, product related feature routes could be `/products`, `/products/:id`, `products/:id/edit`.

To route with code, use angular's `Router` service:
```
this.router.navigate(['/welcome']);
```

Behind the scenes, the `routerLink` directive calls the `Router`'s `navigate` method to route.

We can use the shortcut syntax if the link parameters array contains static strings: `this.router.navigate('/welcome')`

Use `this.router.navigateByUrl('/welcome')` to navigate by complete url path (removes all secondary route information.

Any explicit route definitions defined in a module are placed after the route definitions of imported modules. So if you define a wildcard `**` route in app.component, then import feature modules, the feature module routes come first in the route order and the `**` route will come after them.

But if you define your routes in a different module (like AppRoutingModule) and import them, them the order of the routes will be according to the order of the imports, so be careful about the ordering in that situation,


## Route Parameters
Routes configurations with placeholders (like id) look like this: 
```
[
  {path: 'products/:id', component: ProductDetailComponent}
]
```

Populate the route parameters in the link parameters array like this: `<a [routerLink]="['/products', product.id]">{{product.name}}</a>`

Use the `ActivatedRoute` service to read information (url segments, route parameters, query params, resolver data etc.) from a url in a component:
```
constructor(private route: ActivatedRoute) {
 
 console.log(this.route.snapshot.paramMap.get('id'));
}
```
The paramMap is also available as an observable.

If only the parameters of the url change, the component is not initialized again. So be careful about reading parameters defining parameter dependent component behavior in `ngOnInit`.

You can subscribe to the paramMap observable of the `ActivatedRoute` service to watch for changes like this:
```
this.route.paramMap.subscribe(params => {
  console.log(params.get('id'));
});
```

 Optional parameters are defined in the link parameters array as key-value pairs: `<a [routerLink]="['/products', {name: productName, startDate: startDate, endDate: endDate}]">Search</a>`.
They must come after all required parameters.
In the resulting url, they are separated by a `;`

To read optional parameters, use the same `ActivatedRoute` service:
```
constructor(private route: ActivatedRoute) {  
  console.log('this.route.snapshot.paramMap.get('name')'); 
  console.log('this.route.snapshot.paramMap.get('startDate')');
}
```

Query parameters are also optional, but unlike the optional parameters discussed above, they can be retained across routing paths. Use the `queryParams` directive along with `routerLink` to pass query parameters: `<a [routerLink]="['/products', 'search']" [queryParams]="{filterBy: 'er', showImage: true}">Search</a>`

When routing in code, add a second argument to `router.navigate()`: `this.router.navigate(['/products'], {queryParams: {filterBy: 'er', showImage: true}})`

Query params aren't automatically retained though. To do that, set `queryParamsHandling="preserve"`. For example: `<a routerLink='/products' queryParamsHandling="preserve">Back</a>`

To read query parameters, user the `queryParamMap` (instead of `paramMap`) in the `ActivatedRoute` service: `console.log(this.route.snapshot.queryParamMap.get('filterBy'));`
This is also available as an observable just like `paramMap`.


## Prefetching Data Using Route Resolvers
A route definition has a data property that we can use to prove any data (as key value pairs via an object) to a route:
```
RouterModule.forChild([
  path: 'proudcts',
  component: ProductListComponent,
  data: {pageTitle: 'Product List'}
])
```
This data doesn't change for the lifetime of the application, so we can only use it for static data.

To access the passed in data in the component, use the `ActivatedRoute` service again: `this.route.snapshot.data['pageTitle']`.

We can use a `RouteResolver` for a component to pre-fetch the data that a component needs. With this approach, the component is only activated when the route resolver gets the data (via a service) and is ready. Meh, why can't we just use loading indicators in the component?

A `RouteResolver` is created as an angular service. You just need to implement the `Resolve` interface.

To add a resolver to a route, add it to the route configuration like this: `{path: 'products/:id', component: ProductDetailComponent, resolve: {product: ProductResolver}}`
We can add any number of resolvers in a route configuration.

To read data from the resolver, use the `data` property of the `ActivatedRoute` service: `this.route.snapshot.data['product']`. This is also available as an observable.


## Child Routes
Child routing is used to display routed component templates within other routed component templates. So we can organize routes and their components by feature area like '/products', and then with child routing, have all product routes ('/products/:id', '/products/search' etc.) display their appropriate component within a root product component through a secondary router outlet.

Child routes are defined in a `children` array of the paren't route configuration:
```
{
  path: 'products/:id/edit',
  component: ProductEditComponent,
  resolve: {product: ProductResolver},
  children: [
    {path: '', reditectTo: 'info', pathMatch: 'full'},
    {path: 'info', component: ProductEditInfoComponent},
    {path: 'tags', component: ProductEditTagsComponent}
  ]
}
```
The child routes extend the route of the parent path so we don't repeat the parent's path in their configuration.

To display a child route in the parent's template, the paren't template must contain a `router-outlet` directive.

You can use absolute or relative paths to activate child routes.
Absolute path: `<a [routerLink]="'/products', product.id, 'edit', 'info'">Info</a>`
Relative path: `<a [routerLink]="['info']">Info</a>`


## Grouping and Component-less Routes
Sometimes we want to define routes under a parent route without defining a shell component with a secondary router outlet. For this we can use componentless routes.
We do this for better organization of routes and lazy loading.

To define a component-less route, just remove the `component` property from the parent configuration:
```
RouterModule.forChild([
{
  path: 'products',
  children: [
    {path: '', component: ProductListComponent},
    {path: ':id', component: ProductDetailComponent},
    {path: ':id/edit', component: ProductEditComponent, children: [...]}
  ]
} 
])
```
So instead of rendering the child components in the parent's router outlet, the router will attempt to render the them in the "next higher level" outlet.


## Styling, Animating, and Watching Routes
Use the `routerLinkActive` directive to apply style classes (space delimited strings) to an element when the corresponding `routerLink` is active:
```
<a [routerLink]="['info']" routerLinkActive="active">
  Basic Information
</a>
```

Use the `routerLinkActiveOptions` directive to specify more options like, for example, whether or not to perform an exact match: `[routerLinkActiveOptions]="{exact: true}"`

You can subscribe to the following routing events: NavigationStart, RoutesRecognized, NavigationEnd, NavigationCancel, NavigationError

To see these events, you need to enable tracing. For this, add an object after the route config array like this: `RouterModule.forRoot([...], {enableTracing: true}`

The angular router has an `events` property that is an observable. You can subscribe to this to listen to routing events in code to display spinners etc.
```
this.router.events.subscribe((routerEvent: Event) => {
  if (routerEvent instanceof NavigationStart) {
    ...
  }
}
```

[thought] While this looks like a useful feature for debugging purposes, it seems like we can accomplish the same thing with `isLoading` like state variables that we initialize in `ngOnInit()`


## Secondary Routes
Secondary router outlets are identified by the `name` attribute: `<router-outlet name="popup"></router-outlet>`.
We can define any number of secondary outlets at the same level of the hierarchy.

To configure secondary routes, add the `outlet` property to the route config:
```
RouterModule.forChild([
  {
    path: 'messages',
    component: MessagesComponent,
    outlet: 'popup'
  }
])
```

To activate a secondary route, use the same `routerLink` directive but with a slight change that looks like the following: `<a [routerLink]="[{ outlets: { popup: ['messages'] } }]"><Messages/a>`
This says "activate the 'messages' path in the popup outlet.


## Route Guards
The angular router provides several types of guards:
- canActivate: guard navigation to a route
- canActivateChild: guard navigation to a child route
- canDeactivate: guard navigation away from a route
- canLoad: prevent asynchronous routing
- resolve: prefetch data before activating a route

Route guards are executed in the following order: canDeactivate (for the current route to determine if the user can leave that route) -> canLoad (before the module is loaded if it is loaded asynchronously) -> canActivateChild -> canActivate -> resolve.
If any guards returns false, all pending guards are cancelled and the requested navigation is cancelled.

A route guard is built as an angular service:
```
@Injectible({ providedIn: 'root' })
export class AuthGuard implements CanActivate {
  canActivate(): boolean { // can also return Observable<boolean>
    ...
  }
}
```

To use the guard on a route, add it to the appropriate property in the route definition like this:
```
  {
    path: 'id',
    component: ProductDetailComponent,
    resolve: { product: ProductResolver },
    canActivate: [AuthGuard]
  }
```
You can add multiple guards on a route.

Adding a guard to a parent route guards each of its children.

The `canActivate` guard checks criteria before activating a route. It is commonly used to limit access to parts of the application (based on authentication/authorization).

To use the cli to create a guard, run `ng g guard <path>/<guard_name>`

The difference between the `canActivate` guard and the `canActivateChild` guard is that the `canActivate` guard will not re-execute if only the child route is changed.

