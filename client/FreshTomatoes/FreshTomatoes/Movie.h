//
//  Movie.h
//  FreshTomatoes
//
//  Created by Demi on 5/11/16.
//  Copyright © 2016 Demiforce. All rights reserved.
//

#import <Foundation/Foundation.h>

@interface Movie : NSObject

@property (nonatomic) NSString  *name;
@property (nonatomic) NSString  *thumbnailURL;
@property (nonatomic) float     rating;
@property (nonatomic) NSString  *movieDescription;

@end
