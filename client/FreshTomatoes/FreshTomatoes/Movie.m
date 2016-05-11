//
//  Movie.m
//  FreshTomatoes
//
//  Created by Demi on 5/11/16.
//  Copyright © 2016 Demiforce. All rights reserved.
//

#import "Movie.h"

@implementation Movie

- (NSString*) description
{
    return [NSString stringWithFormat:@"<%@: %p: name=%@>", [self class], self, _name];
}

@end
